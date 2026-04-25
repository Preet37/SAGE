# Source: https://docs.pytorch.org/audio/stable/generated/torchaudio.save_with_torchcodec.html
# Title: torchaudio.save_with_torchcodec — PyTorch/TorchAudio API Reference
# Fetched via: jina
# Date: 2026-04-09

Title: torchaudio.save_with_torchcodec — Torchaudio 2.10.0 documentation


torchaudio.save_with_torchcodec(_uri:[Union](https://docs.python.org/3/library/typing.html#typing.Union "(in Python v3.14)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),[PathLike](https://docs.python.org/3/library/os.html#os.PathLike "(in Python v3.14)")]_, _src:[Tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "(in PyTorch v2.8)")_, _sample\_rate:[int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_, _channels\_first:[bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")=True_, _format:[Optional](https://docs.python.org/3/library/typing.html#typing.Optional "(in Python v3.14)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]=None_, _encoding:[Optional](https://docs.python.org/3/library/typing.html#typing.Optional "(in Python v3.14)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]=None_, _bits\_per\_sample:[Optional](https://docs.python.org/3/library/typing.html#typing.Optional "(in Python v3.14)")[[int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")]=None_, _buffer\_size:[int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")=4096_, _backend:[Optional](https://docs.python.org/3/library/typing.html#typing.Optional "(in Python v3.14)")[[str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")]=None_, _compression:[Optional](https://docs.python.org/3/library/typing.html#typing.Optional "(in Python v3.14)")[[Union](https://docs.python.org/3/library/typing.html#typing.Union "(in Python v3.14)")[[float](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)"),[int](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")]]=None_)→[None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)")[[source]](https://docs.pytorch.org/audio/stable/_modules/torchaudio/_torchcodec.html#save_with_torchcodec)[¶](https://docs.pytorch.org/audio/stable/generated/torchaudio.save_with_torchcodec.html#torchaudio.save_with_torchcodec "Permalink to this definition")
Save audio data to file using TorchCodec’s AudioEncoder.

Note

This function supports the same API as [`save()`](https://docs.pytorch.org/audio/stable/generated/torchaudio.save.html#torchaudio.save "torchaudio.save"), and relies on TorchCodec’s encoding capabilities under the hood. It is provided for convenience, but we do recommend that you port your code to natively use `torchcodec`’s `AudioEncoder` class for better performance: [https://docs.pytorch.org/torchcodec/stable/generated/torchcodec.encoders.AudioEncoder](https://docs.pytorch.org/torchcodec/stable/generated/torchcodec.encoders.AudioEncoder). As of TorchAudio 2.9, [`save()`](https://docs.pytorch.org/audio/stable/generated/torchaudio.save.html#torchaudio.save "torchaudio.save") relies on [`save_with_torchcodec()`](https://docs.pytorch.org/audio/stable/generated/torchaudio.save_with_torchcodec.html#torchaudio.save_with_torchcodec "torchaudio.save_with_torchcodec"). Note that some parameters of [`save()`](https://docs.pytorch.org/audio/stable/generated/torchaudio.save.html#torchaudio.save "torchaudio.save"), like `format`, `encoding`, `bits_per_sample`, `buffer_size`, and `backend`, are ignored by are ignored by [`save_with_torchcodec()`](https://docs.pytorch.org/audio/stable/generated/torchaudio.save_with_torchcodec.html#torchaudio.save_with_torchcodec "torchaudio.save_with_torchcodec"). To install torchcodec, follow the instructions at [https://github.com/pytorch/torchcodec#installing-torchcodec](https://github.com/pytorch/torchcodec#installing-torchcodec).

This function provides a TorchCodec-based alternative to torchaudio.save with the same API. TorchCodec’s AudioEncoder provides efficient encoding with FFmpeg under the hood.

Parameters
*   **uri** (_path-like object_) – Path to save the audio file. The file extension determines the format.

*   **src** ([_torch.Tensor_](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor "(in PyTorch v2.8)")) – Audio data to save. Must be a 1D or 2D tensor with float32 values in the range [-1, 1]. If 2D, shape should be [channel, time] when channels_first=True, or [time, channel] when channels_first=False.

*   **sample_rate** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")) – Sample rate of the audio data.

*   **channels_first** ([_bool_](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)")_,_ _optional_) – Indicates whether the input tensor has channels as the first dimension. If True, expects [channel, time]. If False, expects [time, channel]. Default: True.

*   **format** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_or_ _None_ _,_ _optional_) – Audio format hint. Not used by TorchCodec (format is determined by file extension). A warning is issued if provided. Default: None.

*   **encoding** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_or_ _None_ _,_ _optional_) – Audio encoding. Not fully supported by TorchCodec AudioEncoder. A warning is issued if provided. Default: None.

*   **bits_per_sample** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_or_ _None_ _,_ _optional_) – Bits per sample. Not directly supported by TorchCodec AudioEncoder. A warning is issued if provided. Default: None.

*   **buffer_size** ([_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_,_ _optional_) – Not used by TorchCodec AudioEncoder. Provided for API compatibility. A warning is issued if not default value. Default: 4096.

*   **backend** ([_str_](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")_or_ _None_ _,_ _optional_) – Not used by TorchCodec AudioEncoder. Provided for API compatibility. A warning is issued if provided. Default: None.

*   **compression** ([_float_](https://docs.python.org/3/library/functions.html#float "(in Python v3.14)")_,_[_int_](https://docs.python.org/3/library/functions.html#int "(in Python v3.14)")_or_ _None_ _,_ _optional_) – Compression level or bit rate. Maps to bit_rate parameter in TorchCodec AudioEncoder. Default: None.

Raises
*   [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError "(in Python v3.14)") – If torchcodec is not available.

*   [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError "(in Python v3.14)") – If input parameters are invalid.

*   [**RuntimeError**](https://docs.python.org/3/library/exceptions.html#RuntimeError "(in Python v3.14)") – If TorchCodec fails to encode the audio.

Note

*   TorchCodec AudioEncoder expects float32 samples in [-1, 1] range.

*   Some parameters (format, encoding, bits_per_sample, buffer_size, backend) are not used by TorchCodec but are provided for API compatibility.

*   The output format is determined by the file extension in the uri.

*   TorchCodec uses FFmpeg under the hood for encoding.