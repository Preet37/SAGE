# Source: https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf
# Title: [PDF] Rigid Body Dynamics Algorithms
# Fetched via: search
# Date: 2026-04-09

Preface
The purpose of this book is to present a substantial collection of the most
efficient algorithms for calculating rigid-body dynamics, and to explain them
in enough detail that the reader can understand how they work, and how to
adapt them (or create new algorithms) to suit the reader’s needs. The collection
includes the following well-known algorithms: the recursive Newton-Euler algo-
rithm, the composite-rigid-body algorithm and the articulated-body algorithm.
It also includes algorithms for kinematic loops and floating bases. Each algo-
rithm is derived from first principles, and is presented both as a set of equations
and as a pseudocode program, the latter being designed for easy translation into
any suitable programming language.
This book also explains some of the mathematical techniques used to for-
mulate the equations of motion for a rigid-body system. In particular, it shows
how to express dynamics using six-dimensional (6D) vectors, and it explains the
recursive formulations that are the basis of the most efficient algorithms. Other
topics include: how to construct a computer model of a rigid-body system; ex-
ploiting sparsity in the inertia matrix; the concept of articulated-body inertia;
the sources of rounding error in dynamics calculations; and the dynamics of
physical contact and impact between rigid bodies.
Rigid-body dynamics has a tendency to become a sea of algebra. However,
this is largely the result of using 3D vectors, and it can be remedied by using a
6D vector notation instead. This book uses a notation based on spatial vectors,
in which the linear and angular aspects of rigid-body motion are combined into
a unified set of quantities and equations. The result is typically a four- to six-

…

became clear that there was enough new material to justify the writing of a
whole new book. Compared with its predecessor, the most notable new mate-
rials to be found here are: explicit pseudocode descriptions of the algorithms;
a chapter on how to model rigid-body systems; algorithms to exploit branch-
induced sparsity; an enlarged treatment of kinematic loops and floating-base
systems; planar vectors (the planar equivalent of spatial vectors); numerical
errors and model sensitivity; and guidance on how to implement spatial-vector
arithmetic.

…

38
3
Dynamics of Rigid Body Systems
39
3.1
Equations of Motion . . . . . . . . . . . . . . . . . . . . . . . . .
40
3.2
Constructing Equations of Motion
. . . . . . . . . . . . . . . . .

…

case, a computer is calculating the forces, accelerations, and so on, associated
with the motion of a rigid-body approximation of a physical system.
The main purpose of this book is to present a collection of efficient algo-
rithms for performing various dynamics calculations on a computer. Each al-
gorithm is described in detail, so that the reader can understand how it works
and why it is efficient; and basic concepts are explained, such as recursive for-
mulation, branch-induced sparsity and articulated-body inertia.
Rigid-body dynamics is usually expressed using 3D vectors. However, the
subject of this book is dynamics algorithms, and this subject is better expressed
using 6D vectors. We therefore adopt a 6D notation based on spatial vectors,

…

book. It says a little about dynamics algorithms, a little about spatial vectors,
and it explains how the book is organized.
1.1
Dynamics Algorithms
The dynamics of a rigid-body system is described its equation of motion, which
specifies the relationship between the forces acting on the system and the ac-
celerations they produce. A dynamics algorithm is a procedure for calculating
the numeric values of quantities that are relevant to the dynamics. We will be
concerned mainly with algorithms for two particular calculations:
2
CHAPTER 1. INTRODUCTION
forward dynamics: the calculation of the acceleration response of a given
rigid-body system to a given applied force; and
inverse dynamics: the calculation of the force that must be applied to a given
rigid-body system in order to produce a given acceleration response.
Forward dynamics is used mainly in simulation. Inverse dynamics has a variety
of uses, such as: motion control systems, trajectory planning, mechanical de-
sign, and as a component in a forward-dynamics calculation. In Chapter 9 we
will consider a third kind of calculation, called hybrid dynamics, in which some
of the acceleration and force variables are given and the task is to calculate the
rest.
The equation of motion for a rigid-body system can be written in the fol-
lowing canonical form:
τ = H(q) ¨q + C(q, ˙q) .
(1.1)
In this equation, q, ˙q and ¨q are vectors of position, velocity and acceleration
variables, respectively, and τ is a vector of applied forces. H is a matrix of
inertia terms, and is written H(q) to show that it is a function of q. C is a
vector of force terms that account for the Coriolis and centrifugal forces, gravity,
and any other forces acting on the system other than those in τ. It is written
C(q, ˙q) to show that it depends on both q and ˙q. Together, H and C are the
coefficients of the equation of motion, and τ and ¨q are the variables. Typically,
one of the variables is given and the other is unknown.
Although it is customary to write H(q) and C(q, ˙q), it would be more accu-

…

in which they are connected together, and the values of every parameter as-
sociated with each component (inertia parameters, geometric parameters, and
so on). We call this description a system model in order to distinguish it from
a mathematical model. The difference is this: a system model describes the
system itself, whereas a mathematical model describes some aspect of its be-
haviour. Equation 1.1 is a mathematical model. On a computer, model would
be a variable of type ‘system model’, and its value would be a data structure
containing the system model of a specific rigid-body system.
Let us encapsulate the forward and inverse dynamics calculations into a pair
of functions, FD and ID. These functions satisfy
¨q = FD(model, q, ˙q, τ)
(1.2)
and
τ = ID(model, q, ˙q, ¨q) .
(1.3)
On comparing these equations with Eq. 1.1, it is obvious that FD and ID must
evaluate to H−1(τ −C) and H¨q +C, respectively. However, the point of these
1.2. SPATIAL VECTORS
3
equations is that they show clearly the inputs and outputs of each calculation.
In particular, they show that the system model is an input in both cases. Thus,
there is an expectation that the algorithms implementing FD and ID will work
for a class of rigid-body systems, and will use the data in the system model to
work out the dynamics of the particular rigid-body system described by that
model. We shall use the name model-based algorithm to refer to algorithms that
work like this.
The big advantage of this approach is that a single piece of computer code
can be written, tested, documented, and so on, to calculate the dynamics of any
rigid-body system in a broad class. The two main classes of interest are called
kinematic trees and closed-loop systems. Roughly speaking, a kinematic tree
is any rigid-body system that does not contain kinematic loops, and a closed-
loop system is any rigid-body system that is not a kinematic tree.1 Calculating
the dynamics of a kinematic tree is significantly easier than for a closed-loop
system.
Model-based algorithms can be classified according to their two main at-
tributes: what calculation they perform, and what class of system they apply
to. The main body of algorithms in this book consists of forward and inverse
dynamics algorithms for kinematic trees and closed-loop systems.
1.2
Spatial Vectors
A rigid body in 3D space has six degrees of motion freedom; yet we usually
express its dynamics using 3D vectors. Thus, to state the equation of motion
for a rigid body, we must actually state two vector equations:
f = m aC
and
nC = I ˙ω + ω × Iω .
(1.4)
The first expresses the relationship between the force applied to the body and
the linear acceleration of its centre of mass. The second expresses the relation-
ship between the moment applied to the body, referred to its centre of mass,
and its angular acceleration.
In spatial vector notation, we use 6D vectors that combine the linear and
angular aspects of rigid-body motion. Thus, linear and angular acceleration are
combined to form a spatial acceleration vector, force and moment are combined
to form a spatial force vector, and so on. Using spatial notation, the equation
of motion for a rigid body can be written
f = Ia + v ×∗Iv ,
(1.5)
where f is the spatial force acting on the body, v and a are the body’s spatial
velocity and acceleration, and I is the body’s spatial inertia tensor. The symbol
×∗denotes a spatial vector cross product. One obvious feature of this equation
1A precise definition will be given in Chapter 4, including a definition of ‘kinematic loop.’

…

rigid body, then the spatial inertia of the new body is given by the simple
formula
Inew = I1 + I2 ,
where I1 and I2 are the inertias of the two original bodies.
This equation
replaces three in the 3D vector approach: one to compute the new mass, one to

…

self-contained.
Chapter 2 describes spatial vector algebra from first principles; and Chapter
3 explains how to formulate and analyse the equations of motion for a rigid-
body system. These are the two most mathematical chapters, and they both
cover their subject matter in greater depth than the minimum required for the
algorithms that follow. Chapter 4 describes the various components of a system
model. Many of the quantities used in later chapters are defined here.
Chapters 5, 6 and 7 describe the three best known algorithms for kine-
matic trees: the recursive Newton-Euler algorithm for inverse dynamics, and the
composite-rigid-body and articulated-body algorithms for forward dynamics, in
that order. Chapter 5 also explains the concept of recursive formulation, which
is the reason for the efficiency of these algorithms. Chapter 8 then presents
several techniques for calculating the dynamics of closed-loop systems. These
four chapters are arranged approximately in order of increasing complexity (i.e.,
the algorithms get progressively more complicated).
Chapters 9, 10 and 11 then tackle a variety of extra topics. Chapter 9 consid-
ers several more algorithms, including hybrids of forward and inverse dynamics
and algorithms for floating-base systems. Chapter 10 considers the issues of
numerical accuracy and computational efficiency; and Chapter 11 examines the
dynamics of rigid-body systems that are subject to contacts and impacts.
Readers will find examples dotted unevenly throughout the text. In some

…

Chapter 2
Spatial Vector Algebra
Spatial vectors are 6D vectors that combine the linear and angular aspects of
rigid-body motions and forces. They provide a compact notation for studying
rigid-body dynamics, in which a single spatial vector can do the work of two
3D vectors, and a single spatial equation replaces two (or sometimes more)

…

the equation of motion for a single rigid body. It also presents the planar vector
algebra, which is an adaptation of spatial vector algebra to rigid bodies that
move only in a 2D plane. Methods of implementing spatial vector arithmetic
are covered in Appendix A; and the use of spatial vectors to analyse general

…

describe rigid-body dynamics are Euclidean vectors. Spatial vectors are not
Euclidean, but are instead the elements of a pair of vector spaces: one for
motion vectors and one for forces. Spatial motion vectors describe attributes of
rigid-body motion, such as velocity and acceleration, while spatial force vectors
describe force, impulse and momentum. The two spaces M6 and F6 are the

of Rigid Body Dynamics Algorithms
Justin Carpentier and Nicolas Mansard
Laboratoire d’Analyse et d’Architecture des Syst`emes and Universit´e de Toulouse
Email: justin.carpentier@laas.fr
Abstract—Rigid body dynamics is a well-established frame-
-work in robotics. It can be used to expose the analytic
form
of
kinematic
and
dynamic
functions
of
the
robot
model. So far, two major algorithms, namely the recursive
Newton-Euler algorithm (RNEA) and the articulated body
algorithm (ABA), have been proposed to compute the inverse
dynamics and the forward dynamics in a few microseconds.
Evaluating their derivatives is an important challenge for various
robotic applications (optimal control, estimation, co-design or
reinforcement learning). However it remains time consuming,
whether using finite differences or automatic differentiation. In
this paper, we propose new algorithms to efficiently compute
them thanks to closed-form formulations. Using the chain rule
and adequate algebraic differentiation of spatial algebra, we
firstly differentiate explicitly RNEA. Then, using properties about
the derivative of function composition, we show that the same
algorithm can also be used to compute the derivatives of ABA
with a marginal additional cost. For this purpose, we introduce
a new algorithm to compute the inverse of the joint-space

…

kinematic and dynamic quantities that describe the motion of
poly-articulated systems. Rigid body dynamics algorithms are
for example crucial for the control and the stabilization of
quadruped and humanoid robots [10, 15, 17]. Additionally,
optimal control and trajectory optimization are becoming
standard approaches to control complex robotic systems [26,

…

parameters and control variables of the system. A large part of
the total computational cost of such optimization algorithms
(up to 90 %) is spent in computing these derivatives.
This work is supported by the RoboCom++ FLAG-ERA JTC 2016 proposal
and the European project MEMMO (GA-780684).
Evaluating the partial derivatives of the dynamics can
be performed in several manners. The simplest way is to
approximate them by finite differences, i.e. evaluating several
times the input dynamics while adding a small increment on
the input variables. The main advantage is to systematize the
derivation process by considering the function to differentiate

…

Another methodology is to analytically derive the Lagrangian
equation of motion [11]. Lagrangian derivation gives a better
insight into the structure of the derivatives but leads to
dense computations. It fails to exploit efficiently the sparsity
induced by the kinematic model, in a similar way than rigid

…

the chain rule formula in an automatic way knowing the
derivatives of basic functions (cos, sin or exp), to obtain the
partial derivatives. Automatic differentiation typically requires
intermediate computations which are hard to avoid or to
simplify. Using code generation [12] can mitigate this issue
but is a costly technological process to set up.
In this paper, we rather propose to analytically derive
the rigid-body-dynamics algorithms in order to speed up the
computation of the derivatives. Our formulation provides a
better insight into the mathematical structure of the derivatives.
We are then able to exploit the inherent structure of spatial
algebra (e.g. the cross product operator) at the root of

…

source implementation on which our benchmarks are based.
This paper is made of two concomitant contributions.
In a first contribution we establish in a concise way
the analytical derivatives of the inverse dynamics through
the differentiation of the so-called recursive Newton-Euler
algorithm (RNEA) [19, 7]. The second contribution concerns
the analytical derivatives of the forward dynamics. Rather than
Fig. 1: Spatial notations used all along this paper.
computing the derivatives of the articulated body algorithm
(ABA), we demonstrate that these derivatives can be directly
deduced from the derivatives of the inverse dynamics with only
a minor additional cost. This implies to compute the inverse
of the joint space inertia matrix, for which we also introduce
an original algorithm. We implement all these derivatives
inside our C++ framework for rigid-body systems called
Pinocchio [5].
Based on the standard notations of rigid-body dynamics
(recalled in Sec. II), we make explicit in Sec. III the
partial derivatives of the recursive Newton-Euler algorithm
(RNEA). Sec. IV then explains how the derivatives of the
forward dynamics can be computed from RNEA derivatives.
Benchmarks are reported in Sec. V.
II. RIGID BODY DYNAMICS NOTATIONS
Spatial algebra allows to write in a concise manner the
kinematic (velocity, acceleration, etc.) and dynamic (force,
momenta, etc.) quantities that describe the motion of a rigid

…

angular velocities of the rigid body. In a similar way, we can
define the spatial acceleration of a rigid body, denoted by ai
as the time derivative of the spatial velocity.
3) Kinetic quantities: If the rigid body is also provided
with a mass distribution, we may define its spatial inertia
Ii characterized by the mass, the center of mass and the
rotational inertia of the body. This spatial inertia enables
us to introduce two additional quantities which quantify the
dynamic properties of the rigid body: (i) the spatial momentum
given by hi
def
= Iivi which stacks the linear and angular
momenta expressed in the body frame; (ii) the spatial force

…

III. ANALYTICAL DERIVATIVES OF THE RECURSIVE
NEWTON-EULER ALGORITHM
In this section, we derive the analytical expressions of the
partial derivatives of the inverse dynamics function, denoted
by ID, in the context of rigid-body systems. Inverse dynamics
allows to compute the generalized torque τ to apply on a
rigid-body system (model) in order to produce a desired
generalized acceleration ¨q giving the current generalized
position q and velocity ˙q of the system together with the stack
of external forces f ext:
τ = ID(model, q, ˙q, ¨q, f ext)

…

∂˙q , ∂ID
∂¨q using spatial notations while
avoiding complex computations as the aforementioned tensor
expressions.
A. The recursive Newton-Euler algorithm
As previously mentioned, RNEA recalled in Algorithm 1,
is the most effective way to solve the inverse dynamics
problem by exploiting the structured sparsity induced by the
kinematic model. It is a two-pass algorithm which propagates
the kinematic quantities in a first forward pass (similar to a
forward kinematics), then collect the torque contribution of the
subtrees in a second backward pass. Compared to Featherstone
[7, p. 96], we assume here that the external contact forces are

…

sake of clarity, we separate the derivations for the forward and
the backward passes. All derivations are done with respect to
the generic variable u, which might be with qi or ˙qi. The
expressions are later specialized for qi and ˙qi.
1) Partial derivatives of the forward pass: Algorithm 2

…

The same rule applies for the spatial inertias Ii on line 6.
2) Partial derivatives of the backward pass: Algorithm 3
depicts how the partial derivatives of the joint torque
∂τi
∂u
are affected by the variations of Si and the variation of the
force-set supported by joint i. This backward loop mostly

…

C. Simplifying expressions
Depending on the value of u, some partial derivatives in
Algorithms 2 or 3 vanish because they are independent from
either q or ˙q. We now detail these simplifications in order
to give at the end, a complete and applicable version of the
recursive derivatives. This is certainly the most technical part

…

D. Direct outcome of these derivations
Finally, a direct outcome of these computations is the
analytical expressions of the partial derivatives of the forward
kinematics, through the quantities
∂vi
∂q ,
∂vi
∂˙q
and
∂ai
∂q , ∂ai

…

DYNAMICS
Forward dynamics, denoted by FD, is the reciprocal of
inverse dynamics. In other words, it computes the generalized
acceleration ¨q of the rigid-body system according to the
current generalized position q, velocity ˙q, torque input τ and
external forces f ext:
¨q = FD(model, q, ˙q, τ, f ext)
Using the Lagrangian notations, the forward dynamics reads:
¨q = M −1(q)
�
τ −C(q, ˙q) ˙q −g(q) +
�
i
JT
i (q)f ext
i
�
(15)
Similarly to inverse dynamics, efficient recursive rigid-body

…

corresponds to a backward pass where the spatial forces which
act on bodies are computed from the joint torque input. In
the last recursion, the spatial accelerations of bodies are then
deduced, allowing to compute the joint acceleration vector.
A. Lagrangian expressions of the partial derivatives of the
forward dynamics

…

(i) we already mentioned in Sec. III the difficulties to
explicitly compute the tensors quantities
∂C
∂q , ∂C
∂˙q
and
∂M
∂q . A similar comment holds for ∂M −1
∂q
which can also
be deduced from ∂M
∂q through the relation:
∂M −1
∂q
= −M −1 ∂M
∂q M −1
(ii) from Eq. (10b) and Eq. (16b), we can observe that the
partial derivatives of the inverse and forward dynamics

…

(19)
and for convenience in the notations, we set:
¨q0
def
= FD(model, q0, ˙q0, τ0)
(20)
We omit here the dependency on external forces f ext for better
readability. Applying the chain rule formula on (19), we obtain
the following point-wise equality:
∂ID
∂u
���
q0, ˙q0,¨q0
+ ∂ID
∂¨q
���
q0, ˙q0,¨q0
∂FD
∂u
���
q0, ˙q0,τ0 = ∂τ0

…

It follows from (17) and (24) that the partial derivatives
of the forward dynamics can be directly deduced from
the derivatives of the inverse dynamics. To the best of
our knowledge, this is the first time that this specific
relation between the partial derivatives of forward and inverse
dynamics is highlighted and exploited in order to simplify the
underlying computations.
To summarize the proposed approach, we have shown that
it is sufficient to compute the inverse of the joint space inertia
matrix and the partial derivatives of inverse dynamics, in order
to get the partial derivatives of the forward dynamics. It is
also important to notice at this stage that, if we have already
computed the partial derivatives of the forward dynamics, it is
then possible to directly deduce the partial derivatives of the
inverse dynamics from these quantities. This is made possible
through the inherent relations (18) and (24) that link together
the inverse and forward dynamics as well as their partial
derivatives.
C. Computing the inverse of the joint space inertia matrix
The last difficulty lies in the computation of the inverse
of the joint space inertia matrix denoted M −1. The standard
approach consists in first computing the joint space inertia
matrix M
using CRBA and then performing its sparse
Cholesky decomposition by employing a dedicated algorithm

…

To overcome these limitations, we have developed a
dedicated algorithm to efficiently compute M −1 by exploiting
the sparsity induced by the kinematic tree, and without
requiring the computation of M itself. This algorithm is a
rewriting of ABA where we have omitted the affine terms
like Coriolis and gravity effects that are normally evaluated

…

computing M −1 with this algorithm is in practice up to twice
faster than the Cholesky decomposition for robots equipped
with numerous degrees of freedom, as illustrated in Sec. V.
V. RESULTS
In this section, we report the performances of our analytical
derivatives compared to the finite differences approach. We

From Particles to Rigid Bodies
•
Particles
– No rotations
– Linear velocity v only
– 3N DoFs
•
Rigid bodies
– 6 DoFs (translation + rotation)
– Linear velocity v
– Angular velocity ω

COMP768- M.Lin
Outline
• Rigid Body Representation
• Kinematics
• Dynamics
• Simulation Algorithm
• Collisions and Contact Response
COMP768- M.Lin
Coordinate Systems
• Body Space (Local Coordinate System)
– Rigid bodies are defined relative to this system
– Center of mass is the origin (for convenience)
• We will specify body-related physical properties (inertia, …) 
in this frame
Body Space

COMP768- M.Lin
Coordinate Systems
• World Space:
rigid body transformation to common frame
World Space
rotation
translation

…

COMP768- M.Lin
Rotations
• Rotation matrix
– 3x3 matrix: 9 DoFs
– Columns: world-space coordinates of body-
space base vectors
– Rotate a vector:
Image ETHZ 2005

COMP768- M.Lin
Rotations
• Problem with rotation matrices: numerical 
drift
• Fix: use Gram-Schmidt orthogonalization
• Drift is easier to fix with quaternions
COMP768- M.Lin
Unit Quaternion Definition
• q = [s,v] : s is a scalar, v is vector
• A rotation of θ about a unit axis u can be 
represented by the unit quaternion:
[cos(θ/2), sin(θ /2) u] 
• Rotate a vector: 
• Fix drift: 
– 4-tuple: vector representation of rotation
– Normalized quaternion always defines a rotation in ℜ3
u
θ
COMP768- M.Lin
Unit Quaternion Operations
• Special multiplication:
• Back to rotation matrix

COMP768- M.Lin
Outline
• Rigid Body Representation
• Kinematics
• Dynamics
• Simulation Algorithm
• Collisions and Contact Response

COMP768- M.Lin
• How do x(t) and R(t) change over time?
• Linear velocity v(t) describes the velocity 
of the center of mass x (m/s)
Kinematics: Velocities
Angular velocity
Linear velocity
COMP768- M.Lin
Kinematics: Velocities
• Angular velocity, represented by ω(t) 
– Direction: axis of rotation
– Magnitude |ω|: angular
velocity about the axis 
(rad/s)
• Time derivative of rotation matrix:
– Velocities of the body-frame axes, i.e. the 
columns of R
Image ETHZ 2005
COMP768- M.Lin
Angular Velocities

COMP768- M.Lin
Outline
• Rigid Body Representation
• Kinematics
• Dynamics
• Simulation Algorithm
• Collisions and Contact Response

COMP768- M.Lin
Dynamics: Accelerations
• How do v(t) and ω(t) change over time?
• First we need some more machinery
– Forces and Torques
– Linear and angular momentum
– Inertia Tensor
• Simplify equations by formulating 
accelerations in terms of momentum 
derivatives instead of velocity derivatives
ri
fi
COMP768- M.Lin
• External forces fi(t) act on particles
– Total external force F=∑ fi(t)
• Torques depend on distance from the center 
of mass:
   
 
τi(t) = (ri(t) – x(t)) × fi(t)
– Total external torque 
 
 
τ(t) = ∑ ((ri(t)-x(t)) × fi(t)
• F(t) doesn’t convey any information 
about where the various forces act
•  τ(t) does tell us about the distribution of 
forces
Forces and Torques
COMP768- M.Lin
• Linear momentum P(t) lets us express the effect of 
total force F(t) on body (due to conservation of 
energy): 
 
• Linear momentum is the product of mass and linear 
velocity
– P(t) =∑ midri(t)/dt 
 
=∑ miv(t) + ω(t) × ∑mi(ri(t)-x(t))

…

COMP768- M.Lin
• Same thing, angular momentum L(t) 
allows us to express the effect of total 
torque τ(t) on the body: 
 
• Similarily, there is a linear relationship 
between momentum and velocity:
 
 
– I(t) is inertia tensor, plays the role of mass
• Use L(t) instead of ω(t) in state vectors
Angular momentum
COMP768- M.Lin
Inertia Tensor
• 3x3 matrix describing how the shape and 
mass distribution of the body affects the 
relationship between the angular velocity 
and the angular momentum L(t)
• Analogous to mass – rotational mass
• We actually want the inverse I-1(t) to 
compute ω(t)=I-1(t)L(t)

…

COMP768- M.Lin
Inertia Tensor
• Avoid recomputing inverse of inertia tensor
• Compute I in body space Ibody and then 
transform to world space as required
– I(t) varies in world space, but Ibody is constant in body 
space for the entire simulation
• Intuitively:
– Transform ω(t) to body space, apply inertia tensor in 
body space, and transform back to world space
– L(t)=I(t)ω(t)= R(t) Ibody RT(t) ω(t) 
– I-1(t)= R(t) Ibody
-1 RT(t)
COMP768- M.Lin
Computing Ibody
-1
• There exists an orientation in body space which 
causes Ixy, Ixz, Iyz to all vanish
– Diagonalize tensor matrix, define the eigenvectors to 
be the local body axes
– Increases efficiency and trivial inverse
• Point sampling within the bounding box
• Projection and evaluation of Greene’s thm.
– Code implementing this method exists
– Refer to Mirtich’s paper at
    http://www.acm.org/jgt/papers/Mirtich96
COMP768- M.Lin
Approximation w/ Point 
• Pros: Simple, fairly accurate, no B-rep 
needed.
• Cons: Expensive, requires volume test.

COMP768- M.Lin
Use of Green’s Theorem
• Pros: Simple, exact, no volumes needed.
• Cons: Requires boundary representation.
COMP768- M.Lin
Outline
• Rigid Body Representation
• Kinematics
• Dynamics
• Simulation Algorithm
• Collisions and Contact Response

COMP768- M.Lin
Position state vector
v(t) replaced by linear momentum P(t)
ω(t) replaced by angular momentum L(t)
Size of the vector: (3+4+3+3)N = 13N
Spatial information
Velocity information

…

COMP768- M.Lin
Outline
• Rigid Body Representation
• Kinematics
• Dynamics
• Simulation Algorithm
• Collision Detection and Contact Determination
– Contact classification
– Intersection testing, bisection, and nearest features

COMP768- M.Lin
What happens when bodies collide?
• Colliding
– Bodies bounce off each other
– Elasticity governs ‘bounciness’
– Motion of bodies changes discontinuously within 
a discrete time step
– ‘Before’ and ‘After’ states need to be computed
• In contact
– Resting
– Sliding
– Friction

…

COMP768- M.Lin
Distance(A,B)
• Returns a value which is the minimum distance 
between two bodies
• Approximate may be ok
• Negative if the bodies intersect
• Convex polyhedra
– Lin-Canny and GJK -- 2 classes of algorithms 
• Non-convex polyhedra
– Much more useful but hard to get distance fast
– PQP/RAPID/SWIFT++
• Remark: most of these algorithms give inaccurate 
information if bodies intersect, except for DEEP

…

COMP768- M.Lin
Colliding contacts
• At time ti, body A and B intersect and
 
vrel < -ε
• Discontinuity in velocity: need to stop 
numerical solver
• Find time of collision tc
• Compute new velocities v+(tc)  X+(t)
• Restart ODE solver at time tc with new 
state X+(t)

…

COMP768- M.Lin
Bisection
findCollisionTime(X,t,Δt)   
foreach pair of bodies (A,B) do
 
Compute_New_Body_States(Scopy, t, Δt);
 
hs(A,B) = Δt;    // H is the target timestep
 
if Distance(A,B) < 0 then
try_h = Δt /2;   try_t = t + try_h;
 
    while TRUE do
 
 
Compute_New_Body_States(Scopy, t, try_t - t);
 
 
if Distance(A,B) < 0 then
 
 
 
try_h /= 2;   try_t -= try_h;
 
 
else if Distance(A,B) < ε then
 
 
 
break;
 
 
else
 
 
 
try_h /= 2;   try_t += try_h;
 
    hs(A,B)->append(try_t – t);
    h = min( hs );

…

COMP768- M.Lin
Colliding Contact Response
• Point velocities at the nearest points:
• Relative contact normal velocity:

COMP768- M.Lin
Colliding Contact Response
• We will use the empirical law of 
frictionless collisions:
– Coefficient of restitution є [0,1]
• є = 0 – bodies stick together
• є = 1 – loss-less rebound
• After some manipulation of equations...
COMP768- M.Lin
Compute and apply impulses
•
The impulse is an instantaneous 
force – it changes the velocities of 
the bodies instantaneously:

COMP768- M.Lin
Penalty Methods
• If we don’t look for time of collision tc then 
we have a simulation based on penalty 
methods: the objects are allowed to 
intersect.
• Global or local response
– Global: The penetration depth is used to 
compute a spring constant which forces them 
apart (dynamic springs)
– Local: Impulse-based techniques

son with NADS.
2. A Quick Primer
Rigid body simulation is analogous to the numerical solu-
tion of nonlinear ordinary differential equations for which
closed-form solutions do not exist.
Assume time t is the in-
dependent variable.
Given a time period of interest [t0, tN],
driving inputs, and the initial state of the system, the dif-
ferential equations (the instantaneous-time model) are dis-
cretized in time to yield an approximate discrete-time model,
typically in the form of a system of (state-dependent) al-
gebraic equations and inequalities.
The discrete-time model
is formulated and solved at each time of interest, (t0,..,tN).
In rigid body simulation, one begins with the Newton-Euler
(differential) equations, which describes the dynamic motion
J. Bender et al.
/ Interactive Rigid Body Simulation
of the bodies without contact.
These differential equations
are then augmented with three types of conditions: nonpene-
tration constraints that prevent the bodies from overlapping,
a friction model that requires contact forces to remain within
their friction cones, and complementarity (or variational in-
…
tion that will most quickly halt the sliding.
Putting all these
components together yields the instantaneous-time model,
as a system of differential algebraic equations and inequali-
ties that can be reformulated as a differential nonlinear com-
plementarity problem (dNCP).
The dNCP cannot be solved
in closed form or directly, so instead, one discretizes it in
…
the NCPs and a choice of solution method.
There are many
options for instance reformulation as nonsmooth equation
using Fischer-Burmeister function or proximal point map-
pings etc.
2.1.
Classical Mechanics
Simulation of the motion of a system of rigid bodies is based
on a famous system of differential equations, the Newton-
…
ally, constraints are functions of generalized position vari-
ables, generalized velocities, and their derivatives to any or-
der:
C(q1,q2,u1,u2, ˙u1, ˙u2,...,t) = 0
(2)
or
C(q1,q2,u1,u2, ˙u1, ˙u2,...,t) ≥ 0
(3)
where the subscripts indicate the body.
Equality and inequal-
ity constraints are referred to as bilateral and unilateral con-
straints, respectively.
As an example, consider two rigid spheres of radii r1 and
r2 and with centers located at x1 and x2.
Consider the con-
…
tion of the relative contact velocity.
The Coulomb model has two conditions: first, the net con-
tact force must lie in a quadratic friction cone (see the gray
cone in Figure 6(a)) and second, when the bodies are slip-
ping, the friction force must be the one that directly opposes
…
2.1.5.
The Newton-Euler Equations
The Newton-Euler equations are obtained by applying New-
ton’s second law twice; once for translational motion and
again for rotational motion.
Specifically, the net force F ap-
plied to the body is equal to the time rate of change of trans-
lational momentum mv (i.e., d
dt (mv) = F) and the net mo-
ment τ is equal to the time rate of change of rotational mo-
mentum Iω (i.e., d
dt (Iω) = τ).
Specializing these equations
to the case of a rigid body (which, by definition, has constant
…
yields an equivalent expression with equivalent complexity.
The Newton-Euler equations contain the net force F and
moment τ.
F is simply the vector sum of all forces acting on
the body.
τ is the vector sum of the moments of all the forces
and pure moments.
One can see from equation (7), that the
…
way.
The gyroscopic moments tend to cause the axis of ro-
tation of a rotating rigid body to “precess” about a circular
cone.
Simulation of free body motion is done by integrating
the Newton-Euler equations (7,8) and the velocity kinematic
equation (1) simultaneously.
If there are contacts and joints,
then these equations must be augmented with the constraint
equations (2,3).
If in addition, dry friction exists in contacts,
then equations (4,5,6) must be included.
The complete sys-
tem of differential and algebraic equations and inequalities is
challenging to integrate, but methods to do this robustly have
…
infinite accelerations, which makes direct numerical integra-
tion of the Newton-Euler equations impossible.
One way to
deal with this problem during simulation is to use a stan-
dard integration method up to the time of impact, then use
an impulse-momentum law to determine the jump disconti-
nuities in the velocities, and finally restart the integrator.
Let [t,t + ∆t] be a time step during which a collision oc-
curs.
Further, define p =
� t+∆t
t
Fdt as the impulse of the
net force and mv as translational momentum.
Integrating
equation (7) from t to t + ∆t yields m(v(t + ∆t) − v(t)) =
� t+∆t
t
Fdt, which states that impulse of the net applied force
equals the change of translational momentum of the body.
In
rigid body collisions, ∆t approaches zero.
Taking the limit as
∆t goes to zero, one obtains an impulse momentum law that
is applied at the instant of impact to compute post collision
velocities.
Since ∆t goes to zero and the velocities remain
finite, the generalized position of the bodies are fixed during
the impact.
After processing the collision, one has the val-
ues of the generalized positions and velocities, which are the
needed initial conditions to restart the integrator.
Note that
integration of the rotational equation (8) yields an impulse-
momentum law for determining jump discontinuities in the
rotational velocities.
Based on impulse-momentum laws, several algebraic col-
lision rules have been proposed.
Newton’s Hypothesis is
stated in terms of the normal component of the relative ve-
locity of the colliding points just before and just after colli-

part covers the motion of rigid bodies that are completely unconstrained in their allowable motion;
that is, simulations that aren’t concerned about collisions between rigid bodies.
Given any external
forces acting on a rigid body, we’ll show how to simulate the motion of the body in response to these
forces.
The mathematical derivations in these notes are meant to be fairly informal and intuitive.
The second part of the notes tackles the problem of constrained motion that arises when we
regard bodies as solid, and need to disallow inter-penetration.
We enforce these non-penetration
constraints by computing appropriate contact forces between contacting bodies.
Given values for
these contact forces, simulation proceeds exactly as in the unconstrained case: we simply apply all
the forces to the bodies and let the simulation unfold as though the motions of bodies are completely
unconstrained.
If we have computed the contact forces correctly, the resulting motion of the bodies
will be free from inter-penetration.
The computation of these contact forces is the most demanding
component of the entire simulation process.1
1Collision detection (i.e. determining the points of contact between bodies) runs a close second though!
G1
Part I. Unconstrained Rigid Body Dynamics
1
Simulation Basics
This portion of the course notes is geared towards a full implementation of rigid body motion.
In this
section, we’ll show the basic structure for simulating the motion of a rigid body.
In section 2, we’ll
define the terms, concepts, and equations we need to implement a rigid body simulator.
Following
this, we’ll give some code to actually implement the equations we need.
Derivations for some of the
concepts and equations we will be using will be left to appendix A.
The only thing you need to be familiar with at this point are the basic concepts (but not the numer-
ical details) of solving ordinary differential equations.
If you’re not familiar with this topic, you’re
…
A simulation starts with some initial conditions for Y(0), (i.e. values for x(0) and v(0)) and then
uses a numerical equation solver to track the change or “flow” of Y over time, for as long as we’re
interested in.
If all we want to know is the particle’s location one second from now, we ask the solver
to compute Y(1), assuming that time units are in seconds.
If we’re going to animate the motion of
the particle, we’d want to compute Y( 1
30), Y( 2
30) and so on.
The numerical method used by the solver is relatively unimportant with respect to our actual
…
ence is that the state vector Y(t) for a rigid body holds more information, and the derivative d
dtY(t) is
a little more complicated.
However, we’ll use exactly the same paradigm of tracking the movement
of a rigid body using a solver
ode, which we’ll supply with a function
dydt.
2
Rigid Body Concepts
The goal of this section is to develop an analogue to equation (1–3), for rigid bodies.
The final
differential equation we develop is given in section 2.11.
In order to do this though, we need to define
An Introduction to Physically-Based Modeling
G3
Witkin/Baraff/Kass
a lot of concepts first and relations first.
Some of the longer derivations are found in appendix A.
In
the next section, we’ll show how to write the function
dydt needed by the numerical solver
ode to
compute the derivative d
dtY(t) developed in this section.
2.1
…
thing we need to do is define how the position and orientation change over time.
This means we
need expressions for ˙x(t) and ˙R(t).
Since x(t) is the position of the center of mass in world space,
˙x(t) is the velocity of the center of mass in world space.
We’ll define the linear velocity v(t) as this
…
the directions of the transformed x, y and z body axes at time t.
That means that the columns of ˙R(t)
must describe the velocity with which the x, y, and z axes are being transformed.
To discover the
relationship between ω(t) and R(t), let’s examine how the change of an arbitrary vector in a rigid
…
effects; in particular, ˙r(t) is independent of v(t).
To study ˙r(t), we decompose r(t) into vectors a
and b, where a is parallel to ω(t) and b is perpendicular to ω(t).
Suppose the rigid body were to
maintain a constant angular velocity, so that the tip of r(t) traces out a circle centered on the ω(t) axis
…
y
x
z
x(t)
ω(t)
v(t)
Figure 3: Linear velocity v(t) and angular velocity ω(t) of a rigid body.
Putting this together, we can write ˙r(t) = ω(t) × (b).
However, since r(t) = a + b and a is parallel
…
formation between P(t) and v(t): P(t) = Mv(t) and v(t) = P(t)/M.
Since M is a constant,
˙v(t) =
˙P(t)
M .
(2–28)
The concept of linear momentum lets us express the effect of the total force F(t) on a rigid body
quite simply.
Appendix A derives the relation
˙P(t) = F(t)
(2–29)
which says that the change in linear momentum is equivalent to the total force acting on a body.
Note
that P(t) tells us nothing about the rotational velocity of a body, which is good, because F(t) also
…
angular momentum as a state variable over angular velocity.
For linear momentum, we have the relation P(t) = Mv(t).
Similarly, we define the total angular
momentum L(t) of a rigid body by the equation L(t) = I(t)ω(t), where I(t) is a 3 × 3 matrix (tech-
…


(2–32)
For an actual implementation, we replace the finite sums with integrals over a body’s volume in
world space.
The mass terms mi are replaced by a density function.
At first glance, it seems that
we would need to evaluate these integrals to find I(t) whenever the orientation R(t) changes.
This