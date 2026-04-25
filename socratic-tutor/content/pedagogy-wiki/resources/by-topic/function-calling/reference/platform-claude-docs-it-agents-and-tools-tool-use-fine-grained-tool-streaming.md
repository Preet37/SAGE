# Source: https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming
# Title: Fine-grained tool streaming — Claude API Docs
# Fetched via: trafilatura
# Date: 2026-04-09

Infrastruttura degli strumenti
Trasmetti gli input degli strumenti carattere per carattere per applicazioni sensibili alla latenza.
This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
Lo streaming granulare degli strumenti è generalmente disponibile su tutti i modelli e su tutte le piattaforme. Abilita lo [streaming](/docs/it/build-with-claude/streaming) dei valori dei parametri di utilizzo degli strumenti senza buffering o convalida JSON, riducendo la latenza per iniziare a ricevere parametri di grandi dimensioni.
Quando si utilizza lo streaming granulare degli strumenti, è possibile ricevere input JSON non validi o parziali. Assicurati di tenere conto di questi casi limite nel tuo codice.
Come utilizzare lo streaming granulare degli strumenti
Lo streaming granulare degli strumenti è disponibile su tutti i modelli e su tutte le piattaforme (Claude API, Amazon Bedrock, Google Vertex AI e Microsoft Foundry). Per utilizzarlo, imposta eager_input_streaming
su true
su qualsiasi strumento definito dall'utente in cui desideri abilitare lo streaming granulare e abilita lo streaming sulla tua richiesta.
Ecco un esempio di come utilizzare lo streaming granulare degli strumenti con l'API:
curl https://api.anthropic.com/v1/messages \
-H "content-type: application/json" \
-H "x-api-key: $ANTHROPIC_API_KEY" \
-H "anthropic-version: 2023-06-01" \
-d '{
"model": "claude-opus-4-6",
"max_tokens": 65536,
"tools": [
{
"name": "make_file",
"description": "Write text to a file",
"eager_input_streaming": true,
"input_schema": {
"type": "object",
"properties": {
"filename": {
"type": "string",
"description": "The filename to write text to"
},
"lines_of_text": {
"type": "array",
"description": "An array of lines of text to write to the file"
}
},
"required": ["filename", "lines_of_text"]
}
}
],
"messages": [
{
"role": "user",
"content": "Can you write a long poem and make a file called poem.txt?"
}
],
"stream": true
}'
In questo esempio, lo streaming granulare degli strumenti consente a Claude di trasmettere i versi di una lunga poesia nella chiamata dello strumento make_file
senza buffering per convalidare se il parametro lines_of_text
è un JSON valido. Ciò significa che puoi vedere il parametro trasmesso mentre arriva, senza dover aspettare che l'intero parametro venga memorizzato nel buffer e convalidato.
Con lo streaming granulare degli strumenti, i chunk di utilizzo degli strumenti iniziano a trasmettere più velocemente e spesso sono più lunghi e contengono meno interruzioni di parola. Ciò è dovuto a differenze nel comportamento del chunking.
Esempio:
Senza streaming granulare (ritardo di 15 secondi):
Chunk 1: '{"'
Chunk 2: 'query": "Ty'
Chunk 3: 'peScri'
Chunk 4: 'pt 5.0 5.1 '
Chunk 5: '5.2 5'
Chunk 6: '.3'
Chunk 8: ' new f'
Chunk 9: 'eatur'
...
Con streaming granulare (ritardo di 3 secondi):
Chunk 1: '{"query": "TypeScript 5.0 5.1 5.2 5.3'
Chunk 2: ' new features comparison'
Poiché lo streaming granulare invia parametri senza buffering o convalida JSON, non c'è garanzia che il flusso risultante si completi in una stringa JSON valida.
In particolare, se viene raggiunto il [motivo di arresto](/docs/it/build-with-claude/handling-stop-reasons) max_tokens
, il flusso potrebbe terminare a metà di un parametro e potrebbe essere incompleto. In genere devi scrivere un supporto specifico per gestire quando viene raggiunto max_tokens
.
Accumulo dei delta di input degli strumenti
Quando un blocco di contenuto tool_use
trasmette, l'evento iniziale content_block_start
contiene input: {}
(un oggetto vuoto). Questo è un segnaposto. L'input effettivo arriva come una serie di eventi input_json_delta
, ognuno contenente un frammento di stringa partial_json
. Il tuo codice deve concatenare questi frammenti e analizzare il risultato una volta che il blocco si chiude.
Il contratto di accumulo:
- Su
content_block_start
contype: "tool_use"
, inizializza una stringa vuota:input_json = ""
- Per ogni
content_block_delta
contype: "input_json_delta"
, aggiungi:input_json += event.delta.partial_json
- Su
content_block_stop
, analizza la stringa accumulata:json.loads(input_json)
La mancata corrispondenza di tipo tra l'input: {}
iniziale (oggetto) e partial_json
(stringa) è intenzionale. L'oggetto vuoto contrassegna lo slot nell'array di contenuto; le stringhe delta costruiscono il valore reale.
import json
import anthropic
client = anthropic.Anthropic()
tool_inputs = {} # index -> accumulated JSON string
with client.messages.stream(
model="claude-opus-4-6",
max_tokens=1024,
tools=[
{
"name": "get_weather",
"description": "Get current weather for a city",
"eager_input_streaming": True,
"input_schema": {
"type": "object",
"properties": {"city": {"type": "string"}},
"required": ["city"],
},
}
],
messages=[{"role": "user", "content": "Weather in Paris?"}],
) as stream:
for event in stream:
if (
event.type == "content_block_start"
and event.content_block.type == "tool_use"
):
tool_inputs[event.index] = ""
elif (
event.type == "content_block_delta"
and event.delta.type == "input_json_delta"
):
tool_inputs[event.index] += event.delta.partial_json
elif event.type == "content_block_stop" and event.index in tool_inputs:
parsed = json.loads(tool_inputs[event.index])
print(f"Tool input: {parsed}")
Gli SDK Python e TypeScript forniscono helper di flusso di livello superiore (stream.get_final_message()
, stream.finalMessage()
) che eseguono questo accumulo per te. Utilizza il modello manuale sopra solo quando hai bisogno di reagire all'input parziale prima che il blocco si chiuda, come il rendering di un indicatore di progresso o l'avvio anticipato di una richiesta a valle.
Gestione di JSON non valido nelle risposte degli strumenti
Quando si utilizza lo streaming granulare degli strumenti, è possibile ricevere JSON non valido o incompleto dal modello. Se hai bisogno di passare questo JSON non valido al modello in un blocco di risposta di errore, puoi avvolgerlo in un oggetto JSON per garantire una gestione corretta (con una chiave ragionevole). Ad esempio:
{
"INVALID_JSON": "<your invalid json string>"
}
Questo approccio aiuta il modello a capire che il contenuto è JSON non valido preservando al contempo i dati malformati originali a scopo di debug.
Quando avvolgi JSON non valido, assicurati di eseguire correttamente l'escape di eventuali virgolette o caratteri speciali nella stringa JSON non valida per mantenere una struttura JSON valida nell'oggetto wrapper.
Passaggi successivi
Streaming dei messaggi
Riferimento completo per gli eventi inviati dal server e i tipi di eventi di flusso.
Gestire le chiamate degli strumenti
Esegui gli strumenti e restituisci i risultati nel formato di messaggio richiesto.
Riferimento degli strumenti
Directory completa degli strumenti dello schema Anthropic e delle loro stringhe di versione.
Was this page helpful?