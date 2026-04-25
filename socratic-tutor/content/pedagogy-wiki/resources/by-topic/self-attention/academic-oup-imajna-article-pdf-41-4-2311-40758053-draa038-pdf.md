# Source: https://academic.oup.com/imajna/article-pdf/41/4/2311/40758053/draa038.pdf
# Author: Blanchard, Pierre, Higham, Desmond J, Higham, Nicholas J
# Author Slug: blanchard-pierre-higham-desmond-j-higham-nicholas-j
# Title: IMA Journal of Numerical Analysis (2021) 41, 2311–2330
# Fetched via: search
# Date: 2026-04-11

doi:10.1093/imanum/drz060
Advance Access publication on 13 March 2020
A mixed-primal finite element method for the coupling of
Brinkman–Darcy flow and nonlinear transport
Mario Alvarez
Sección de Matemática, Sede de Occidente, Universidad de Costa Rica,

…

the fluid patterns on the whole domain, and the Brinkman-Darcy equations are coupled to a nonlinear
transport equation accounting for mass balance of the scalar concentration. We introduce a mixed-
primal variational formulation of the problem and establish existence and uniqueness of solution using
fixed-point arguments and small-data assumptions. A family of Galerkin discretizations that produce
divergence-free discrete velocities is also presented and analysed using similar tools to those employed in
the continuous problem. Convergence of the resulting mixed-primal finite element method is proven, and
some numerical examples confirming the theoretical error bounds and illustrating the performance of the
proposed discrete scheme are reported.
Keywords:
nonlinear transport; Brinkman–Darcy coupling; vorticity-based formulation; fixed-point
theory; mixed finite elements; error analysis.
1. Introduction
The aim of this paper is to put together an extension of the results from Alvarez et al. (2015, 2016a)
and Alvarez et al. (2016b) dealing with augmented and fully mixed finite element approximations
of coupled flow and transport problems, and coupled Brinkman and Darcy flow, respectively. The

…

preserving physical properties. Even if many numerical solutions are already available (see, e.g., Khaled
& Vafai, 2003; Ehrhardt et al., 2009; Joodi et al., 2010; Jena et al., 2013 and the references therein) up
to the authors’ knowledge the only contributions addressing mathematical and numerical properties of

…

(2019) and Zhang et al. (2019) focusing on discrete analysis of splitting of time stepping between the
conforming discretizations on the two subdomains.
The main difference of these works with respect to our contribution is that we propose a formulation
of the problem written in terms of Brinkman vorticity and the transmission conditions we employ are
slightly different. In addition, we introduce a mixed-primal finite element method for the Brinkman–
Darcy-transport coupling that produces divergence-free discrete velocities. Another clear motivation
for using a vorticity-based formulation in the Brinkman domain is that the method is pressure-robust;
it computes the vorticity vector directly and avoiding derivative-based postprocessing (this field is of

…

compared to other mixed formulations using for instance vorticity tensors. These features are essentially
inherited from other schemes such as the methods for Stokes or Brinkman equations advanced in Anaya
et al. (2013, 2016) and Vassilevski & Villa (2014).
Following our previous work (Alvarez et al., 2016b) the coupling of subdomains is based on a
vorticity-based fully mixed formulation for the Brinkman–Darcy problem, whereas a primal formulation
for the transport problem is adapted from Alvarez et al. (2016a). The solvability of such a coupling will
be based on extending the fixed-point strategy introduced in Alvarez et al. (2015) and Alvarez et al.

…

techniques to recover H1(Ω) velocities. Instead, a different smoothness assumption is introduced at
the level of the continuous analysis of the transport problem and subsequently in the solvability of
the Brinkman–Darcy-transport coupling. More precisely, the derivation of existence of weak solutions
relies on a strategy combining classical fixed-point arguments, suitable regularity assumptions on the
decoupled problems, the Lax–Milgram lemma, preliminary results from Alvarez et al. (2016b) and the
Sobolev embedding and Rellich–Kondrachov compactness theorems. In addition, sufficiently small data
allow us to establish uniqueness of weak solution. On the other hand, the well posedness of the discrete
problem is based on the Brouwer fixed-point theorem and analogous arguments to those employed in
the continuous analysis. Finally, similar arguments as those utilized in Alvarez et al. (2016a,b) allow
Downloaded from https://academic.oup.com/imajna/article/41/1/381/5771306 by Monash University user on 23 January 2021
A MIXED-PRIMAL FINITE ELEMENT METHOD
383
us to derive the corresponding Céa estimates for both the Brinkman–Darcy and transport problems, and
these lead to natural a priori error bounds for the Galerkin scheme.
Outline. This paper has been structured as follows. The remainder of this section presents some
notation and preliminary definitions of spaces needed thereafter. The model problem along with
boundary data are stated in Section 2. The weak formulation of the problem and its well-posedness
analysis in the framework of the Schauder fixed-point theorem are collected in Section 3. The associated
Galerkin scheme is then proposed in Section 4 and its solvability is established by the Brouwer fixed-
point theorem. Next, we derive in Section 5 some a priori error estimates and conclude in Section 6
with a few numerical examples in 2D and 3D, illustrating the good performance of the mixed-primal
finite element method and confirming the expected error decay.
Preliminaries. Standard notation will be adopted for Lebesgue and Sobolev spaces. In addition, by

…

⎞
⎠if n = 3, and curl v = ∂1v2 −∂2v1 if n = 2.
In addition, we also recall the orthogonal decomposition
L2(Θ) = L2
0(Θ) ⊕P0(Θ),

…

stands for, e.g., temperature). The model problem can be summarized as follows:
(Brinkman)
μK−1
B uB + μ curl ωB + ∇pB = φfB
ωB −curl uB = 0
div uB = 0
⎫

…

in the formulation.
For the sake of our analysis, the variable coefficients need to satisfy the following requirements:
there exist positive constants ϑ1, ϑ2, γ1, γ2, Lϑ and Lfbk, such that
ϑ1 ≤ϑ(s) ≤ϑ2

…

386
M. ALVAREZ ET AL.
In view of deriving a weak form of (2.1)–(2.3) and according to the boundary data (2.4) we introduce
the following functional spaces:
HB(div; ΩB) :=
�
vB ∈H(div; ΩB) :

…

Γ0, such that
∥ψ∥1,Ω ≤cp |ψ|1,Ω,
∀ψ ∈H1
Γ0(Ω).
(2.8)
3. Weak formulation and its solvability analysis
In this section we proceed similarly as in Alvarez et al. (2015) and Alvarez et al. (2016a), to derive
a suitable variational formulation of (2.1)–(2.4) and analyse its solvability by means of a fixed-point
strategy.
3.1
Continuous mixed-primal formulation
The continuity of pressure across the interface allows us to define its trace
λ := pD|Σ = pB|Σ ∈H1/2(Σ).
(3.1)
Then, after testing the Brinkman momentum equation in (2.1) against vB ∈HB(div; ΩB) and integrating
by parts, we get
μ
�
ΩB
K−1
B uB·vB+ μ
�
ΩB
vB·curl ωB−

…

A MIXED-PRIMAL FINITE ELEMENT METHOD
387
On the other hand, testing the first equation of (2.2) with functions in HD(div; ΩD), integrating by parts,
using the boundary conditions and employing (3.1), we get
μ
�
ΩD
K−1
D uD · vD −
�
ΩD
pD div vD −⟨vD · n, λ⟩Σ =
�
ΩD
φfD · vD
∀vD ∈HD(div; ΩD).
In addition, the second equation in (2.2) is tested as

…

�
ΩB
ψfB · vB +
�
ΩD
ψfD · vD
∀⃗v ∈H.
(3.3)
Next, we observe that the solution for (3.2) is not unique. Indeed, it suffices to consider ⃗p := (c, c, c),

…

388
M. ALVAREZ ET AL.
On the other hand, given u in a suitable space (to be made precise in Lemma 3.2, below), testing
with functions in H1
Γ0(Ω), integrating by parts and using the boundary data, we deduce the following

…

C u(φ, ψ) :=
�
Ω
ϑ(φ) ∇φ · ∇ψ −
�
Ω
φ u · ∇ψ +
�
Ω
β φ ψ
∀φ, ψ ∈H1
Γ0(Ω).
(3.6)
The mixed-primal formulation of our original coupled problem (2.1)–(2.3) and (2.4), reduces then

…

3.2
Fixed-point strategy
We describe a fixed-point framework for (3.7). We commence by introducing the operator Sflow :
H1
Γ0(Ω) −→H(div; Ω) defined as
Sflow(φ) := u :=
�
uB
in
ΩB
uD

…

where, given (φ, u) ∈H1
Γ0(Ω) × H(div; Ω), �φ is the unique solution (to be confirmed below) of
the linear advection problem arising from (3.5) after performing the following actions: replacing the
nonlinear expression ϑ(φ) ∇φ appearing in the first term of C u (cf. (3.6)) by the linear one ϑ(φ) ∇�φ;

…

A MIXED-PRIMAL FINITE ELEMENT METHOD
389
that the expression on the right-hand side of (3.5) becomes a linear functional of ψ. In this way, the
aforementioned linear problem reduces to find �φ ∈H1
Γ0(Ω) such that
C φ,u(�φ, �

…

Γ0(Ω), with (⃗u, ⃗p) solving
(3.4) for the given φ, is solution of the original coupled problem (3.7).
3.3
Well posedness of the uncoupled problem
In this section we show that the uncoupled problems (3.4) and (3.8) are in fact well posed. We begin
the solvability analysis with the following result, whose proof is a direct consequence of Alvarez
et al. (2016b, Theorem 3.2). Let us remark that similar vorticity-based formulations for Brinkman–
Darcy equations can be analysed using a different approach, as done recently in Anaya et al. (2019).
Downloaded from https://academic.oup.com/imajna/article/41/1/381/5771306 by Monash University user on 23 January 2021

…

δ ∈(1/2, 1) (when n = 3), such that ∥u∥δ,Ω < r0. Then, the problem (3.8) has a unique solution
Sadv(φ, u) := �φ ∈H1
Γ0(Ω). Moreover, there exists CSadv > 0, independent of (φ, u), such that
∥Sadv(φ, u)∥1,Ω ≤CSadv γ2|Ω|1/2|g|.
(3.15)
Proof.
We first notice that C φ,u (cf. (3.9)) is clearly a bilinear form. In turn, employing the upper
bound of ϑ (cf. (2.5)), Cauchy–Schwarz’s inequality and Hölder’s inequality, it readily follows from

…

Lax–Milgram lemma implies the existence of a unique solution �φ := Sadv(φ, u) ∈H1
Γ0(Ω) of (3.8),
and the corresponding continuous dependence result becomes (3.15) with CSadv = 1
�α =
2c2
p
ϑ1 .
□
Remark 3.3 The bound for ∥u∥δ,Ω used in Lemma 3.2 could also have been taken as
∥u∥δ,Ω < ε
ϑ1
cpCδC∗
δ
,
with any ε ∈(0, 1), however choosing simply ε =
1
2 yields a joint maximization of the ellipticity
constant of C φ,u. In addition, dropping the term β ∥�φ∥2
0,Ω in (3.18) we have assumed that β is small and
then utilized the Poincaré inequality (2.8). When β is instead large, say β ≥ϑ1, then the aforementioned
expression is maintained throughout the derivation of (3.18), implying that the Poincaré inequality (2.8)
is not required.
We end this section by introducing adequate regularity hypotheses on Sflow, which will be employed
to guarantee that the operator T is well defined. In addition, we also assume sufficient regularity of Sadv
in order to establish its Lipschitz continuity and also that of T. In fact, for the remainder of this paper
we follow Alvarez et al. (2016a, Eq. (3.23) and Eq. (3.24)) and consider the following two hypotheses.

…

Lemma 3.2, which is in turn crucial to prove that T is well defined. Subsequently, the estimate
(3.19) is employed in Lemma 3.8 to bound an expression of the form ∥Sflow(φ −ϕ)∥L2p(Ω) in terms
of ∥Sflow(φ −ϕ)∥δ,Ω, and hence depending on the right-hand side of (3.19). In turn, the further
regularity from Hypothesis 3.5 is used in the proof of Lemma 3.7 to bound an expression of the

  ##### Invariant measure of numerical approximation to periodic stochastic differential equations with Markov switchingth MarkYongmei Cai and others

  
  *IMA Journal of Numerical Analysis*, drag011, https://doi.org/10.1093/imanum/drag011
  Published: 6 April 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 31 March 2026

…

  ##### hp -discontinuous Galerkin method for the generalized Burgers–Huxley equation with weakly singular kernelsth weakSumit Mahajan and Arbaz Khan

  
  *IMA Journal of Numerical Analysis*, draf151, https://doi.org/10.1093/imanum/draf151
  Published: 29 March 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 25 March 2026

…

  ##### Error estimates of physics-informed neural networks for approximating Boltzmann equationsroximatElie Abdo and others

  
  *IMA Journal of Numerical Analysis*, draf142, https://doi.org/10.1093/imanum/draf142
  Published: 25 March 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 25 March 2026

…

  ##### Optimal error estimates of mixed finite element methods for SPDEs with gradient-dependent multiplicative noiseent-depYaping Li and others

  
  *IMA Journal of Numerical Analysis*, drag009, https://doi.org/10.1093/imanum/drag009
  Published: 23 March 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 23 March 2026

…

  ##### Skew-symmetric schemes for stochastic differential equations with non-Lipschitz drift: an unadjusted Barker algorithm drift:Yuga Iguchi and others

  
  *IMA Journal of Numerical Analysis*, draf147, https://doi.org/10.1093/imanum/draf147
  Published: 16 March 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 13 March 2026

…

  ##### A hybrid polynomial spectral collocation method for weakly singular Volterra integral equations with variable exponentolterraZheng Ma and Martin Stynes

  
  *IMA Journal of Numerical Analysis*, draf144, https://doi.org/10.1093/imanum/draf144
  Published: 6 March 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 5 March 2026
  ##### Multivariate Newton interpolation in downward closed spaces reaches the optimal Bernstein–Walsh approximation rateches thMichael Hecht and others

  
  *IMA Journal of Numerical Analysis*, draf137, https://doi.org/10.1093/imanum/draf137
  Published: 5 March 2026 **Section: ** ORIGINAL MANUSCRIPT
- Review Article 27 February 2026

…

  ##### A hybrid high-order method for the Gross–Pitaevskii eigenvalue problembrid hiMoritz Hauck and Yizhou Liang

  
  *IMA Journal of Numerical Analysis*, draf126, https://doi.org/10.1093/imanum/draf126
  Published: 16 February 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 13 February 2026

…

  ##### Correction of weighted and shifted seven-step BDF for parabolic equations with nonsmooth dataighted Minghua Chen and others

  
  *IMA Journal of Numerical Analysis*, draf125, https://doi.org/10.1093/imanum/draf125
  Published: 27 January 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 25 January 2026
  ##### Superconvergence analysis for patch-recovered finite element approximations of topological derivativesis for Jiajie Li and others

  
  *IMA Journal of Numerical Analysis*, draf121, https://doi.org/10.1093/imanum/draf121
  Published: 25 January 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 5 January 2026
  ##### An evolving surface finite element method for the Cahn–Hilliard equation with a logarithmic potentialfinite Charles M Elliott and Thomas Sales

  
  *IMA Journal of Numerical Analysis*, draf114, https://doi.org/10.1093/imanum/draf114
  Published: 5 January 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 4 January 2026
  ##### A structure-preserving relaxation Crank–Nicolson finite element method for the Schrödinger–Poisson equationelaxatiHuini Liu and others

  
  *IMA Journal of Numerical Analysis*, draf117, https://doi.org/10.1093/imanum/draf117
  Published: 4 January 2026 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 30 December 2025

…

  ##### A monotone piecewise constant control integration approach for the two-factor uncertain volatility modeliecewisDuy-Minh Dang and Hao Zhou

  
  *IMA Journal of Numerical Analysis*, draf095, https://doi.org/10.1093/imanum/draf095
  Published: 22 December 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 21 December 2025
  ##### Optimal error bounds on an exponential wave integrator Fourier spectral method for the logarithmic Schrödinger equationn exponWeizhu Bao and others

  
  *IMA Journal of Numerical Analysis*, draf108, https://doi.org/10.1093/imanum/draf108
  Published: 21 December 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 17 December 2025
  ##### On the relation between Galerkin approximations and canonical best-approximations of solutions to the Gross–Pitaevskii eigenvalue problemations Muhammad Hassan and others

  
  *IMA Journal of Numerical Analysis*, draf123, https://doi.org/10.1093/imanum/draf123
  Published: 17 December 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 15 December 2025

…

  ##### Analysis of a mixed finite element method for poisson’s equation with rough boundary datacember Huadong Gao and others

  
  *IMA Journal of Numerical Analysis*, draf116, https://doi.org/10.1093/imanum/draf116
  Published: 8 December 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 8 December 2025

…

  ##### Error estimates of finite element methods for nonlocal problems using exact or approximated interaction neighbourhoodsr estimQiang Du and others

  
  *IMA Journal of Numerical Analysis*, draf106, https://doi.org/10.1093/imanum/draf106
  Published: 8 December 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 8 December 2025

…

  ##### Almost conservation of the harmonic actions for fully discretized nonlinear Klein–Gordon equations at low regularityNovembeCharbella Abou Khalil and Joackim Bernier

  
  *IMA Journal of Numerical Analysis*, draf098, https://doi.org/10.1093/imanum/draf098
  Published: 19 November 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 17 November 2025

…

  ##### Weak well-posedness and weak discretization error for stable-driven SDEs with Lebesgue driftL MANUSMathis Fitoussi and others

  
  *IMA Journal of Numerical Analysis*, draf079, https://doi.org/10.1093/imanum/draf079
  Published: 29 October 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 28 October 2025

…

  ##### Time-grid independent error analysis of adaptive predictor-corrector BDF2 scheme for the unsteady Navier–Stokes equations with high Reynolds number##### TBingquan Ji and others

  
  *IMA Journal of Numerical Analysis*, draf094, https://doi.org/10.1093/imanum/draf094
  Published: 27 October 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 19 October 2025

…

  ##### Error analysis of an implicit–explicit time discretization scheme for semilinear wave equations with application to multiscale problemsOctoberDaniel Eckhardt and others

  
  *IMA Journal of Numerical Analysis*, draf092, https://doi.org/10.1093/imanum/draf092
  Published: 14 October 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 8 October 2025

…

  ##### A posteriori error estimates for the generalized Burgers–Huxley equation with weakly singular kernelsGINAL MSumit Mahajan and Arbaz Khan

  
  *IMA Journal of Numerical Analysis*, draf083, https://doi.org/10.1093/imanum/draf083
  Published: 2 October 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 2 October 2025

…

  ##### Combined DG–CG finite element method for the Westervelt equationlished:Sergio Gómez and Vanja Nikolić

  
  *IMA Journal of Numerical Analysis*, draf080, https://doi.org/10.1093/imanum/draf080
  Published: 28 September 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 28 September 2025

…

  ##### Numerical approximation of the stochastic Cahn–Hilliard equation with space–time white noise near the sharp-interface limitL MANUSĽubomír Baňas and Jean Daniel Mukam

  
  *IMA Journal of Numerical Analysis*, draf064, https://doi.org/10.1093/imanum/draf064
  Published: 3 September 2025 **Section: ** Review Article
- Research Article 30 August 2025

…

  ##### Maximum bound principle and original energy dissipation of arbitrarily high-order ETD Runge–Kutta schemes for Allen–Cahn equations ** ORIChaoyu Quan and others

  
  *IMA Journal of Numerical Analysis*, draf069, https://doi.org/10.1093/imanum/draf069
  Published: 10 August 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 2 August 2025

…

  ##### The geometric error is less than the pollution error when solving the high-frequency Helmholtz equation with high-order FEM on curved domains2025 **T Chaumont-Frelet and E A Spence

  
  *IMA Journal of Numerical Analysis*, draf035, https://doi.org/10.1093/imanum/draf035
  Published: 7 July 2025 **Section: ** ORIGINAL MANUSCRIPT
- Research Article 7 July 2025

Crete, Greece.
BUYANG LI ‡
Department of Applied Mathematics, The Hong Kong Polytechnic University, Hong Kong.
[Received on 16 June 2019; revised on 13 March 2020; accepted on 13 March 2020]
The implicit Euler scheme for nonlinear partial differential equations of gradient flows is linearized by
Newton’s method, discretized in space by the finite element method. With two Newton iterations at each
time level, almost optimal order convergence of the numerical solutions is established in both the Lq(Ω)
and W 1,q(Ω) norms. The proof is based on techniques utilizing the resolvent estimate of elliptic operators
on Lq(Ω) and the maximal Lp-regularity of fully discrete finite element solutions on W −1,q(Ω).
Keywords: gradient flow; nonlinear equation; finite element method; linearization; Newton’s iteration;
resolvent estimate; maximal Lp-regularity.
1. Introduction
We consider the following initial and boundary value problem for a time-dependent nonlinear partial

…

Problems of the form (1.1) occur in many applications, including minimal surface flows (cf. [24,
28]), with fff(p) = p/
�
1+|p|2 , regularized models of total variation flows (cf. [8,9,21]), with fff(p) =

…

The nonuniform ellipticity leads to some mathematical difficulties in the numerical analysis of this
problem. In particular, uniform W 1,∞-boundedness of the numerical solutions needs to be proved in the
error estimation in order to rule out the possibility of degeneracy.
Optimal order convergence in the discrete L∞(0,T;L2(Ω)) norm for the implicit Euler scheme,
combined with finite element spatial discretization, for the regularized total variation flow was first
proved in [8,9] by the energy technique. The W 1,∞-boundedness of the numerical solutions was proved
by using an inverse inequality of the finite element space, which requires a stepsize restriction τ = o(h2).

…

the energy approach used in [21] is limited to two-dimensional problems and finite element methods
of polynomial degree r ⩾2. In a general d-dimensional domain, error analysis of semidiscretization in
time was presented in [16] by utilizing the discrete maximal Lp-regularity approach. However, since the
analysis in [16] is based on estimates in the Lp(0,T;W 2,q(Ω)) norm, it cannot be extended to the case
of finite element spatial discretization (as the finite element solutions are not in W 2,q(Ω)).
This article is concerned with full discretization of (1.1) under the local ellipticity condition (1.2), by
using Newton’s iterative method to linearize the nonlinear system obtained by the implicit Euler scheme
with the piecewise linear finite element spatial discretization. We assume that the initial and boundary
value problem (1.1) admits a sufficiently regular solution, and prove almost optimal order convergence
of the numerical solutions with a fixed number of Newton iterations, say ℓiterations at each time level,
in two- and three-dimensional domains without the stepsize restriction τ = o(h2).
Our idea is to split the error of the Newton iterative finite element solutions into three parts:
un
h,ℓ(x)−u(x,tn) = [un(x)−u(x,tn)]+[un
ℓ(x)−un(x)]+[un
h,ℓ(x)−un
ℓ(x)],
(1.4)
where un denotes the time-discrete solution, and un
ℓand un
h,ℓdenote the Newton iterative solutions of
the time-discrete and fully discrete nonlinear systems, respectively. An estimate of the first part on
the right-hand side of (1.4) in the Lp(0,T;W 2,q(Ω))∩W 1,p(0,T;Lq(Ω)) norm was obtained in [16] by
using maximal Lp-regularity of time discretizations of parabolic equations. This estimate provides a

…

ical solutions. The technical tools we use are the Lp(0,T;W 1,q(Ω)) estimate of discretized parabolic
equations, i.e., estimates (2.15)–(2.16)), and the best approximation property of finite element approx-
imations to parabolic equations in the discrete Lp(0,T;Lq(Ω)) norm, i.e., estimate (2.18). Both tools
are consequences of the discrete maximal Lp-regularity theory [4, 10, 13–15, 17, 19, 20, 22], which is a
mathematical tool for numerical analysis of nonlinear parabolic equations; see [1, 2, 16, 18, 26]. These
articles are mainly concerned with either semidiscretization in time or semilinear parabolic equations;
the techniques cannot be applied to the strongly nonlinear problem of gradient flow with fully discrete
numerical methods, especially in the case involving linearization by Newton’s iterations.
In Section 2, we introduce the linearized Newton iterative finite element method for (1.1). Then,
we present the main theoretical result on the convergence of the numerical solutions. Using resolvent
estimates of elliptic operators on Lq(Ω), in Section 3 we establish error estimates for the time-discrete
Newton iterative solutions in W 2,q(Ω) and W 1,∞(Ω). Then, we view the fully discrete Newton iterative
solutions as spatial finite element approximations of the time-discrete Newton iterative solutions, and
estimate the difference between the two solutions in Section 4. Under this point of view, we prove

…

un ∈W 1,∞(Ω) ∩H1
0(Ω) to the nodal values u(tn) := u(·,tn) of the exact solution, by discretizing (1.1)
with the implicit Euler scheme,
un −un−1
τ
= ∇· fff(∇un),

…

4 of 21
where u0
h ∈Sh is the L2 projection of the initial value u0.
The implicit Euler scheme (2.6) and its finite element discretization (2.7) are nonlinear equations
that cannot be implemented directly. An efficient way to linearize (2.6), as well as the corresponding
fully discrete scheme (2.7), is by Newton’s method.
2.2
Linearization by Newton’s method
Let
Dfff(p) := ∇p fff(p),
D2 fff(p) := ∇2
p fff(p)
and
D3 fff(p) := ∇3

…

h,ℓthe L2 projection of the initial value u0.
Alternatively, (2.9) can also be viewed as the finite element discretization of the semidiscrete Newton
iteration scheme (2.8). Based on this point of view, the error of the Newton iterative finite element
solutions given by (2.9) can be split into the three parts in (1.4) that can be estimated separately.
The main result of this paper is the following theorem.
THEOREM 2.1 Let ℓ⩾2. Then, under assumptions (a1)–(a3), there exist positive constants τ⋆and h⋆
such that for τ ⩽τ⋆and h ⩽h⋆the numerical solutions given by the Newton iterative finite element

…

if p = ∞.
The main technical tool is the following theorem on discrete maximal Lp-regularity of fully discrete
finite element solutions of parabolic equations with time-dependent coefficients.
THEOREM 2.2 Let q > d and ai j = aji ∈C([0,T];W 1,q(Ω)), i, j = 1,...,d, be functions satisfying (2.1)

…

0(Ω).
(2.19)
REMARK 2.1 Estimates (2.15) and (2.16) can be viewed as maximal Lp-regularity on the Banach space
W −1,s(Ω) for fully discrete and semidiscrete schemes, respectively.
Under the assumptions of Theorem 2.2, the Ritz projection satisfies the following estimate (cf. [5,

…

6 of 21
3. Newton’s iteration for time discretization
Under assumptions (a1)–(a3), it has been proved in [16, Theorem 2.1] that the semidiscrete solutions
un,n = 1,...,N, are well defined and satisfy the following estimate:

…

(3.1)
where q is the number in assumption (a1). This further implies the following regularity estimate (for the
time-discrete solution):
max
1⩽n⩽N
�
∥δτun∥W 1,∞+∥un∥W 2,q
�
⩽c,
(3.2)
where δτun = (un −un−1)/τ. This regularity estimate plays a crucial role in our analysis of Newton’s
method applied to both the implicit Euler scheme (2.6) and its finite element discretization (2.7).
The main result of this section is the following proposition.
PROPOSITION 3.1 Let ℓ⩾2. Then, under assumptions (a1)–(a3), there exists a positive constant τ0 such
that for τ ⩽τ0 the numerical solutions given by the Newton iterative scheme (2.8) satisfy the following

…

(3.21)
which further implies
∥en
m∥W 1,∞(Ω) ⩽c∥en
m∥W 2,q(Ω) ⩽cτ.
(3.22)
For sufficiently small τ, the last two estimates imply (3.13)–(3.14), completing the second loop of

# Volume 41, Issue 4, October 2021
# Volum#### Articles, October##### Accurately computing the log-sum-exp and softmax functions###Pierre Blanchard and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2311–2330, https://doi.org/10.1093/imanum/draa038
##### Error analysis and uncertainty quantification for the heterogeneous transport equation in slab geometryntiIvan G Graham and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2331–2361, https://doi.org/10.1093/imanum/draa028
##### An unfitted hybrid high-order method for the Stokes interface problem###Erik Burman and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2362–2387, https://doi.org/10.1093/imanum/draa059
##### On the convergence of a finite volume method for the Navier–Stokes–Fourier system thEduard Feireisl and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2388–2422, https://doi.org/10.1093/imanum/draa060
##### Post-processing of the planewave approximation of Schrödinger equations.
Part I: linear operatorsng Eric Cancès and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2423–2455, https://doi.org/10.1093/imanum/draa044
##### Post-processing of the plane-wave approximation of Schrödinger equations.
Part II: Kohn–Sham modelsssiGeneviève Dusson
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2456–2487, https://doi.org/10.1093/imanum/draa052
…
##### On QZ steps with perfect shifts and computing the index of a differential-algebraic equation
#Nicola Mastronardi and Paul Van Dooren
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2516–2529, https://doi.org/10.1093/imanum/draa049
##### Finite difference approach to fourth-order linear boundary-value problems3/iMatania Ben-Artzi and Benjamin Kramer
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2530–2561, https://doi.org/10.1093/imanum/draa057
…
##### Adaptive quarkonial domain decomposition methods for elliptic partial differential equationsdraStephan Dahlke and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2608–2638, https://doi.org/10.1093/imanum/draa030
##### Optimal finite element error estimates for an optimal control problem governed by the wave equation with controls of bounded variation elSebastian Engel and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2639–2667, https://doi.org/10.1093/imanum/draa032
##### Weak and strong error analysis of recursive quantization: a general approach with an application to jump diffusions
Gilles Pagès and Abass Sagna
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2668–2707, https://doi.org/10.1093/imanum/draa033
##### A Banach space mixed formulation for the unsteady Brinkman–Forchheimer equationss:/Sergio Caucao and Ivan Yotov
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2708–2743, https://doi.org/10.1093/imanum/draa035
…
##### A second-order discretization for degenerate systems of stochastic differential equationsps:Yuga Iguchi and Toshihiro Yamada
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2782–2829, https://doi.org/10.1093/imanum/draa039
##### On best constants in L 2 approximation, VAndrea Bressan and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2830–2840, https://doi.org/10.1093/imanum/draa041
##### Anderson acceleration for contractive and noncontractive operatorsctoSara Pollock and Leo G Rebholz
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2841–2872, https://doi.org/10.1093/imanum/draa095
##### An adaptively enriched coarse space for Schwarz preconditioners for P 1 discontinuous Galerkin multiscale finite element problemsum/Erik Eikeland and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2873–2895, https://doi.org/10.1093/imanum/draa043
…
##### Range-relaxed criteria for choosing the Lagrange multipliers in the Levenberg–Marquardt method021A Leitão and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2962–2989, https://doi.org/10.1093/imanum/draa050
##### Analysis of an interior penalty DG method for the quad-curl problem*, Gang Chen and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 2990–3023, https://doi.org/10.1093/imanum/draa034
##### Fast algorithm for the three-dimensional Poisson equation in infinite domainslumChunxiong Zheng and Xiang Ma
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 3024–3045, https://doi.org/10.1093/imanum/draa051
##### Fully discrete finite element approximation of the stochastic Cahn–Hilliard–Navier–Stokes system 4,G Deugoué and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 3046–3112, https://doi.org/10.1093/imanum/draa056
##### Higher-order discontinuous Galerkin time discretizations for the evolutionary Navier–Stokes equations 4,Naveed Ahmed and Gunar Matthies
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 3113–3144, https://doi.org/10.1093/imanum/draa053
##### A sharp error estimate of piecewise polynomial collocation for nonlocal problems with weakly singular kernels OcMinghua Chen and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 3145–3174, https://doi.org/10.1093/imanum/draa054
##### Optimal error estimates and recovery technique of a mixed finite element method for nonlinear thermistor equations OcHuadong Gao and others
*IMA Journal of Numerical Analysis*, Volume 41, Issue 4, October 2021, Pages 3175–3200, https://doi.org/10.1093/imanum/draa063
- ** Front Matter
- ** Table of Contents
- ** Back Matter

convexity constraints.
The method utilizes bubble functions as key analytical tools, eliminating
the need for stabilizers typically used in traditional WG methods and leading to a more streamlined
formulation.
The proposed method is symmetric, positive definite, and easy to implement.
Optimal-
order error estimates are derived for the WG approximations in the discrete H1-norm, assuming the
…
Its strength lies in leveraging weak derivatives and weak continuities to design numer-
ical schemes grounded in the weak forms of underlying PDEs.
A significant develop-
ment within the WG framework is the Primal-Dual Weak Galerkin (PDWG) method
[21, 22, 4, 5, 6, 23, 39, 40, 61, 8, 44, 45, 43, 46, 47].
PDWG formulates numeri-
cal solutions as constrained minimizations of functionals, where the constraints are
derived from the weak formulation of PDEs using weak derivatives.
This approach
leads to an Euler-Lagrange system that incorporates both the primal variable and the
dual variable (Lagrange multiplier), resulting in a symmetric and efficient numerical
…
higher-degree polynomials for computing the discrete weak strain tensor and discrete
weak divergence.
Despite this requirement, our method preserves the size and global
sparsity of the stiffness matrix, significantly reducing programming complexity com-
pared to traditional stabilizer-dependent WG methods.
Theoretical analysis demon-
strates that the WG approximations achieve optimal error estimates in the discrete
…
auto-stabilized weak Galerkin scheme, detailing its construction and features.
Section
4 establishes the theoretical groundwork by proving the existence and uniqueness of
the solution for the algorithm developed in Section 3.
In Section 5, we derive the
error equation associated with the method, which leads naturally to Section 6, where
error estimates in the energy norm are rigorously analyzed.
Finally, Section 7 presents
numerical experiments that corroborate the theoretical results and demonstrate the
effectiveness of the proposed approach.
Throughout this paper, we adopt standard notations.
Let D represent any open
bounded domain in Rd with a Lipschitz continuous boundary.
The inner product,
…
Let u denote the exact solution of the elasticity interface problem (1.1), and let
uh ∈Vh represent its numerical approximation obtained from the auto-stabilized WG
Algorithm 3.1.
The error function eh is defined as:
(5.3)
eh = u −uh ∈V 0
…
Proof.
Using the definitions of µ and λ (the Lam´e constants), (2.2), the Cauchy-
Schwarz inequality, the trace inequalities (4.1)-(4.2), and the estimate (6.3) with n = k
and s = 0, 1, we obtain:
…
i=1
∥u∥2
k+1,Ωi
���
T ∈Th
∥ϵw(u −Qhu)∥2
T
�1
2 .
(6.5)
Using (2.4), the Cauchy-Schwarz inequality, the trace inequalities (4.1)-(4.2), and
the estimate (6.3) with n = k and s = 0, 1, we have
…
i=1[Hk+1(Ωi)]d.
Then, there exists a
constant C > 0, such that the following error estimate holds:
(6.7)
|||u −uh||| ≤Chk
�N
�
i=1
∥u∥2
k+1,Ωi
�
.
Proof. For the right-hand side of the error equation (5.4), we apply the Cauchy-
Schwarz inequality, the trace inequality (4.1), the estimates (6.1)-(6.2) with m = k+1