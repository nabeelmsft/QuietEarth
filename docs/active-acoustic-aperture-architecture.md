# Active Acoustic Aperture Architecture

## Document Status

| Attribute | Status |
|---|---|
| Architecture status | Proposed engineering architecture |
| Physical acoustic principle | Validated at one fixed error-microphone location |
| Autonomous control-state search | Validated using recorded physical measurements |
| Live closed-loop control | Not validated |
| Physical Active Acoustic Aperture | Not validated |
| Datacenter field validation | Not completed |
| Production readiness | Not established |

This document connects QuietEarth's physical evidence from Experiment 003 and controller behavior from Experiment 004 to the proposed Active Acoustic Aperture architecture for AI datacenter cooling infrastructure.

The architecture described here is a proposed engineering direction. It is not a claim of operational datacenter, outdoor, property-boundary, or residential validation.

---

## 1. North Star

QuietEarth's long-term objective is:

> Reduce persistent tonal noise radiated by AI datacenter cooling infrastructure before that noise propagates into surrounding communities, while preserving cooling airflow, compute capacity, cooling performance, and datacenter reliability.

The human-centered success criterion remains:

> QuietEarth succeeds when residents can no longer perceive or identify datacenter hum under representative worst-case listening conditions.

The project does not define success solely as a numerical reduction measured near the noise source. Final success must be evaluated where the environmental impact occurs, including property boundaries and nearby residences.

---

## 2. Problem Context

AI datacenter cooling equipment requires substantial and continuously available airflow. Fans, heat-rejection equipment, air-handling systems, and related infrastructure may produce persistent tonal components that propagate through cooling outlets and other acoustic radiation paths.

Conventional mitigation can introduce undesirable tradeoffs, including:

- airflow restriction
- increased static pressure
- cooling-efficiency loss
- larger physical footprint
- operational changes
- dependence on community-side mitigation

QuietEarth investigates whether persistent tonal acoustic energy can instead be controlled at the acoustic escape path while leaving required cooling airflow available.

---

## 3. Active Acoustic Aperture Concept

The Active Acoustic Aperture is a proposed retrofit acoustic-control layer positioned at or near a datacenter cooling-system acoustic radiation path.

Its intended purpose is to:

1. allow required cooling airflow to continue through an open path
2. identify persistent tonal acoustic components
3. generate a synchronized counteracting acoustic field
4. measure the residual tonal field
5. search for the lowest-residual control state
6. verify that the selected state is repeatable
7. maintain the selected state while conditions remain acceptable
8. reacquire a new control state when acoustic conditions change

The Active Acoustic Aperture is not intended to change:

- fan speed
- cooling setpoints
- compute workloads
- datacenter capacity
- equipment operating points

The number, type, placement, output capability, and acoustic characteristics of aperture control elements and microphones have not yet been determined for a datacenter implementation.

---

## 4. Conceptual System Architecture

```text
AI Datacenter Cooling Equipment
        |
        | cooling airflow
        | persistent tonal acoustic energy
        v
Reference Acoustic Sensing
        |
        | detected tonal frequencies
        | timing and acoustic-state information
        v
QuietEarth Edge Controller
        |
        | DETECT dominant tonal components
        | SEARCH control state
        | VERIFY measured attenuation
        | MAINTAIN acceptable state
        | REACQUIRE when residual rises
        |
        | future control dimensions:
        |   phase
        |   amplitude
        |   delay
        |   control-source coordination
        v
=================================================
           ACTIVE ACOUSTIC APERTURE

     [Control Element]     [Control Element]


              OPEN AIRFLOW PATH


     [Control Element]     [Control Element]

=================================================
        |
        | cooling airflow remains available
        | residual acoustic field propagates outward
        v
Error and Validation Microphones
        |
        +----------------------+
        |                      |
        v                      |
Residual Tonal Measurement    |
        |                      |
        +------ QuietEarth Feedback
        |
        v
Datacenter Boundary
        |
        v
Surrounding Environment
        |
        v
Nearby Community
```

This diagram represents a conceptual architecture. It does not prescribe the final number or physical arrangement of control elements and microphones.

---

## 5. QuietEarth Control Loop

```text
LISTEN
   |
   v
IDENTIFY
persistent tonal components
   |
   v
SEARCH
candidate control states
phase / amplitude / delay
   |
   v
ACT
through aperture control elements
   |
   v
MEASURE
residual tonal energy
   |
   v
VERIFY
with repeated measurements
   |
   v
MAINTAIN
lowest acceptable residual state
   |
   v
Has the residual exceeded
the configured threshold?
       |               |
      NO              YES
       |               |
       v               v
   MAINTAIN        REACQUIRE
                       |
                       v
                     SEARCH
```

Experiment 004 currently demonstrates this reasoning using recorded physical measurements.

Experiment 004 does not yet perform:

- live microphone capture
- synchronized physical audio output
- real-time control adaptation
- live control of aperture elements

---

## 6. Relationship to Experiment 003

Experiment 003 supplied the first controlled physical validation evidence supporting the Active Acoustic Aperture direction.

### 6.1 Physical Signal Chain

```text
Surface Laptop
        |
        | synchronized stereo control signal
        v
Creative Inspire T2900
LEFT and RIGHT loudspeakers
        |
        | physical acoustic propagation through air
        v
Fixed Jabra Error Microphone
        |
        | USB acoustic acquisition
        v
Jetson Xavier
        |
        v
QuietEarth compute_fft()
        |
        v
Measured residual 200 Hz amplitude
```

### 6.2 Experimental Configuration

Experiment 003 used:

- one synchronized stereo playback clock
- two Creative Inspire T2900 loudspeakers
- a 200 Hz sine-wave test signal
- configurable relative phase between stereo channels
- physical acoustic propagation through air
- a fixed Jabra USB error microphone
- Jetson Xavier for acoustic acquisition
- QuietEarth `compute_fft()` for residual-tone measurement

The microphone, speakers, playback volume, acquisition configuration, and geometry were held fixed during the authoritative phase-comparison measurements.

### 6.3 Authoritative Experiment 003 Measurements

| Condition | Measured 200 Hz amplitude |
|---|---:|
| LEFT speaker only | 58.652957 |
| RIGHT speaker only | 52.448952 |
| BOTH 345° | 57.369749 |
| BOTH 0° | 39.933457 |
| BOTH 15° | 29.684351 |
| BOTH 30° | 15.072868 |
| BOTH 45°, Trial 1 | 1.284177 |
| BOTH 45°, Trial 2 | 0.844939 |
| BOTH 45°, Trial 3 | 0.565633 |
| BOTH 180° | 107.806039 |

### 6.4 Repeatability

Three independent recordings were completed at the 45° control setting:

```text
Trial 1: 1.284177
Trial 2: 0.844939
Trial 3: 0.565633
```

The arithmetic mean was:

```text
0.898250
```

The repeated measurements remained substantially below the two individual-speaker reference measurements.

### 6.5 Experiment 003 Conclusion

Experiment 003 demonstrated:

> Repeatable phase-controlled attenuation of a physical 200 Hz acoustic tone at one fixed error-microphone location.

The experiment also demonstrated that changing the synchronized control state can produce either attenuation or reinforcement.

The 180° condition measured `107.806039`, while the three 45° trials measured `1.284177`, `0.844939`, and `0.565633`.

This contrast shows that the residual acoustic field depended strongly on the synchronized physical control state.

### 6.6 Measurement Qualification

The Experiment 003 values are:

- relative experimental FFT amplitudes
- produced through the existing QuietEarth `compute_fft()` path
- suitable for controlled A/B comparison within this experiment

The values are not:

- calibrated dB SPL measurements
- property-boundary measurements
- residential measurements
- evidence of whole-room silence
- evidence of outdoor cancellation
- evidence of datacenter-scale performance

Experiment 003 is the first physical regression oracle for the QuietEarth control architecture.

---

## 7. Relationship to Experiment 004

Experiment 004 converted the Experiment 003 measurement landscape into an autonomous control-state search and verification workflow.

Experiment 004 removed the human decision from the measurement-interpretation layer.

### 7.1 Controller Behavior

Experiment 004:

1. loads a configured tonal-control objective
2. establishes a reference baseline
3. evaluates candidate control states through a measurement-provider interface
4. aggregates repeated measurements
5. selects the tested state with the lowest median residual amplitude
6. verifies the selected state with independent trials
7. calculates relative reduction metrics
8. enters `MAINTAIN` when verification satisfies configured criteria
9. requests `REACQUIRE` when a later residual exceeds the configured threshold

### 7.2 Experiment 004 Results

| Result | Value |
|---|---|
| Target frequency | 200 Hz |
| Selected tested phase | 45° |
| Verification trials | 1.284177, 0.844939, 0.565633 |
| Verification mean | Approximately 0.898250 |
| Verification median | 0.844939 |
| Reported amplitude reduction | 98.559426% |
| Reported amplitude-ratio reduction | 36.829291 dB |
| Controller state after verification | `MAINTAIN` |
| Elevated residual behavior | `REACQUIRE` |
| Measurement source | Recorded physical acoustic measurements |
| Physical acoustic acquisition | `TRUE` |
| Autonomous live control | `FALSE` |
| Active Acoustic Aperture validated | `FALSE` |
| Datacenter field validated | `FALSE` |

The reported decibel value is an amplitude-ratio calculation derived from uncalibrated experimental FFT amplitudes. It is not a calibrated dB SPL measurement.

### 7.3 Measurement-Provider Architecture

The controller operates through a replaceable measurement-provider abstraction.

Current and planned providers include:

- `RecordedMeasurementProvider`
- `SimulationMeasurementProvider`
- future `LiveMicrophoneMeasurementProvider`

This separation is important because the controller should not depend on Experiment 003 data or a specific physical setup.

A future live provider should be able to:

1. capture a fixed-duration microphone window
2. invoke the existing QuietEarth spectral-analysis path
3. measure residual amplitude at the target frequency
4. return the measurement through the same provider interface
5. allow the existing controller search logic to operate without redesign

### 7.4 The 45° Result Is Not Hard-Coded

The 45° control state is not a universal QuietEarth solution.

It was the lowest-residual tested state in the Experiment 003 physical geometry.

A different physical system may require a different combination of:

- phase
- amplitude
- delay
- transducer placement
- microphone placement
- control-source coordination

QuietEarth is intended to search for the measured low-residual state rather than assume that a theoretically ideal or previously successful phase will remain optimal.

---

## 8. Proposed Active Acoustic Aperture Components

A future physical Active Acoustic Aperture may contain the following components.

### 8.1 Reference Sensing

Purpose:

- detect persistent tonal components associated with cooling infrastructure
- provide acoustic timing and spectral information
- distinguish targeted tonal components from unrelated ambient sound

The final number, placement, frequency response, and environmental protection requirements of reference sensors remain to be determined.

### 8.2 QuietEarth Edge Controller

Purpose:

- identify dominant tonal components
- evaluate candidate control states
- coordinate synchronized acoustic-control output
- measure residual energy through error microphones
- verify repeatability
- maintain acceptable control states
- reacquire when conditions change
- remain within configured safety and reliability boundaries

Jetson Xavier has been validated as an edge execution platform for the current QuietEarth software, simulations, physical recording analysis, and recorded-measurement controller MVP.

### 8.3 Aperture Control Elements

Purpose:

- generate a synchronized acoustic-control field
- target persistent tonal components
- operate without blocking the required cooling-airflow path

The final technology may involve one or more types of acoustic actuator.

Experiment 003 used conventional loudspeakers to validate the physical control principle. It did not determine the production actuator technology.

### 8.4 Error Microphones

Purpose:

- measure residual tonal energy
- provide feedback to QuietEarth
- verify the selected control state
- detect acoustic degradation
- initiate reacquisition when necessary

Multiple error microphones are expected to be necessary when extending control beyond one measured location.

### 8.5 Boundary and Validation Sensors

Purpose:

- determine whether mitigation benefits extend beyond the equipment
- detect unintended acoustic amplification
- map attenuation and reinforcement across multiple locations
- validate performance at the datacenter boundary

Community validation would require additional independent measurements beyond the datacenter property.

---

## 9. Fail-Safe and Datacenter Constraints

The following requirements are architectural invariants.

QuietEarth must not:

- reduce datacenter compute capacity
- modify workloads as a noise-control mechanism
- require cooling-setpoint changes as a noise-control mechanism
- require fan-speed changes as a noise-control mechanism
- reduce required cooling airflow
- compromise thermal safety
- interfere with datacenter reliability
- require acoustic equipment at nearby residences
- depend on community-side sound masking
- move objectionable noise from one neighboring area to another
- create unsafe acoustic output levels
- represent simulation or laboratory results as datacenter field validation

The physical aperture should be designed so that loss of QuietEarth power or control does not obstruct required cooling airflow.

Datacenter cooling, thermal safety, and equipment reliability take priority over acoustic mitigation.

The final system requires independent acoustic, electrical, thermal, structural, environmental, and safety review.

---

## 10. Validated Capabilities

The following capabilities have supporting QuietEarth evidence:

- execution on Jetson Xavier
- physical Jabra USB microphone acquisition
- detection of a physical 440 Hz acoustic tone
- detection of a physical 200 Hz acoustic tone
- synchronized stereo control from one playback clock
- independent control of two physical loudspeaker channels
- phase-dependent physical attenuation and reinforcement
- repeatable low-residual measurements at one fixed error-microphone location
- processing through the QuietEarth `compute_fft()` path
- recorded-measurement control-state search
- repeated-trial verification
- `MAINTAIN` controller-state reasoning
- threshold-based `REACQUIRE` reasoning
- explicit separation between physical, simulated, and future live measurements

---

## 11. Proposed and Unvalidated Capabilities

The following capabilities remain proposed and have not been validated:

- live microphone-to-controller integration
- live controller-to-actuator output
- fully closed-loop physical control
- automatic live phase optimization
- automatic live amplitude optimization
- automatic live delay optimization
- multiple simultaneous tonal components
- broadband cooling-noise control
- distributed aperture-mounted control elements
- multiple error microphones
- extended spatial attenuation
- attenuation across the complete aperture
- attenuation at multiple exterior locations
- real fixed-speed cooling-fan attenuation
- physical open-airflow aperture
- preserved airflow under control operation
- static-pressure effects
- cooling-temperature effects
- actuator power requirements
- physical fail-open behavior
- outdoor weather performance
- outdoor acoustic propagation
- datacenter-scale operation
- property-boundary attenuation
- half-mile residential attenuation
- human imperceptibility
- suppression under quiet nighttime conditions
- prevention of amplification at every unprotected location
- production readiness
- regulatory compliance
- patentability

---

## 12. Validation Ladder

```text
Experiment 001
Ideal numerical cancellation
        |
        v
Experiment 002
Propagation-aware numerical control
        |
        v
Experiment 003
Physical phase-controlled attenuation
at one fixed error-microphone location
        |
        v
Experiment 004
Autonomous control-state search
VERIFY / MAINTAIN / REACQUIRE
        |
        v
Live microphone feedback
        |
        v
Live synchronized control output
        |
        v
Automatic phase, amplitude, and delay search
        |
        v
Instrumented open-airflow aperture
        |
        v
Real fixed-speed cooling fan
        |
        v
Multiple aperture-mounted control elements
        |
        v
Multiple exterior error microphones
        |
        v
Spatial attenuation mapping
        |
        v
Airflow validation
        |
        v
Static-pressure validation
        |
        v
Thermal validation
        |
        v
Fail-open hardware validation
        |
        v
Outdoor spatial mapping
        |
        v
Datacenter pilot
        |
        v
Property-boundary validation
        |
        v
Representative residential validation
        |
        v
Resident-centered outcome
```

---

## 13. Next Engineering Milestone

The next recommended engineering milestone is:

> Implement a read-only live microphone measurement provider that captures a fixed-duration acoustic window and calculates the residual amplitude at a target tonal frequency through the existing QuietEarth `compute_fft()` path.

This milestone should preserve the current provider-independent controller architecture.

It should not yet:

- control physical speakers
- control amplifiers
- generate high-amplitude audio
- modify cooling equipment
- claim closed-loop ANC
- claim Active Acoustic Aperture validation

After live measurement is validated, the next milestone is synchronized physical control output with explicit amplitude limits, emergency-stop behavior, and appropriate acoustic-safety review.

---

## 14. Datacenter Validation Path

A credible datacenter validation program should proceed in stages.

### Stage 1: Source Characterization

Determine:

- which cooling assets produce the objectionable tones
- which frequencies dominate at the acoustic radiation path
- whether the tones remain stable or change with operating conditions
- whether the energy is radiated through an opening, equipment surface, structural path, or combination

### Stage 2: Controlled Fan or Ventilation Experiment

Use:

- real fixed-speed fan
- instrumented outlet or duct
- reference microphones
- error microphones
- synchronized control elements
- QuietEarth edge controller

Measure:

- control-off tonal amplitude
- control-on tonal amplitude
- repeatability
- unintended reinforcement
- controller stability

### Stage 3: Open-Airflow Prototype

Validate:

- acoustic attenuation
- airflow rate
- static-pressure change
- temperature change
- actuator power
- fail-open behavior

### Stage 4: Spatial Validation

Use multiple microphones to determine:

- location and size of attenuation zones
- locations where sound remains unchanged
- locations where sound increases
- required number and placement of control elements
- required number and placement of error microphones

### Stage 5: Outdoor Validation

Test:

- distance
- direction
- weather variation
- reflections
- ground effects
- temperature gradients
- wind
- nighttime ambient conditions

### Stage 6: Datacenter Pilot

Validate the system on representative cooling infrastructure without changing:

- fan operating point
- cooling setpoint
- workload
- compute capacity
- cooling capacity
- safety behavior

### Stage 7: Community-Centered Validation

Final validation should determine whether:

- the identifiable tonal hum is reduced at the property boundary
- the identifiable tonal hum is reduced at representative residences
- ordinary field microphones can capture the hum
- residents can perceive or identify the hum
- another neighborhood receives increased acoustic energy
- cooling and compute performance remain unchanged

---

## 15. Architectural Principle

> QuietEarth is not designed to block cooling airflow. It is designed to control persistent tonal acoustic energy at the point where that energy escapes the cooling system, using edge intelligence, synchronized acoustic control, and measured feedback.

> Experiment 003 established that a controllable low-residual physical acoustic state can exist at one fixed error-microphone location under the tested physical geometry. Experiment 004 established that QuietEarth can search for, verify, maintain, and reacquire a low-residual tested state using recorded physical measurement data. The Active Acoustic Aperture is the proposed architecture for extending those capabilities to AI datacenter cooling infrastructure.

The final vision remains:

> AI datacenters should deliver valuable compute without asking neighboring communities to sacrifice peace and quiet.