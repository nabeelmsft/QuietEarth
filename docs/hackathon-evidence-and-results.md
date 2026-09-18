# QuietEarth Hackathon Evidence & Results

**Microsoft Hackathon 2026**

## Canonical Project References

- [Experiment 003 Physical Tonal Attenuation](experiments/experiment-003-physical-tonal-attenuation.md)
- [Active Acoustic Aperture Architecture](active-acoustic-aperture-architecture.md)

## 1\. Executive Summary

QuietEarth is a research proof of concept exploring an **Active Acoustic Aperture** for reducing persistent tonal noise from AI datacenter cooling infrastructure while preserving cooling airflow, cooling performance, compute capacity, and datacenter reliability.

The long\-term human\-centered objective is simple:

**QuietEarth succeeds when residents can no longer perceive or identify datacenter hum under representative worst\-case listening conditions.**

The hackathon did not attempt to claim that outcome has already been achieved at datacenter scale.

Instead, QuietEarth built an evidence ladder from numerical simulation to physical acoustic validation and autonomous control\-state reasoning.

During the hackathon, QuietEarth progressed through four major validation stages:

1. **Experiment 001:** ideal numerical cancellation.
2. **Experiment 002:** propagation\-aware numerical control.
3. **Experiment 003:** repeatable physical phase\-controlled attenuation using real loudspeakers, real acoustic propagation through air, a physical microphone, Jetson Xavier edge hardware, and QuietEarth spectral analysis.
4. **Experiment 004:** autonomous search, verification, MAINTAIN, and REACQUIRE reasoning over recorded physical acoustic measurements.

The strongest physical result came from Experiment 003.

At one fixed error\-microphone location, three independent measurements using the same 45° control state produced residual 200 Hz amplitudes of:

- **1.284177**
- **0.844939**
- **0.565633**

The arithmetic mean was approximately:

**0.898250**

The left\-speaker\-only reference amplitude under the same experiment geometry was:

**58.652957**

These are relative FFT amplitude measurements, not calibrated dB SPL measurements.

The result demonstrates that QuietEarth reached a repeatable, low\-residual physical acoustic state for a controlled 200 Hz tone at one fixed measurement location.

It does **not** demonstrate whole\-room cancellation, outdoor attenuation, operational datacenter performance, airflow preservation, or community\-scale noise elimination.

---

# 2\. The Problem

Large AI datacenters require substantial and continuously available cooling.

Cooling infrastructure can include fans, air\-handling equipment, heat\-rejection systems, pumps, and other mechanical systems capable of producing persistent acoustic tones and harmonics.

Even when overall sound levels are not extreme, a stable and identifiable tonal hum can remain noticeable, particularly in quiet nighttime conditions.

QuietEarth starts from a resident\-centered premise:

The meaningful outcome is not merely a lower numerical measurement near cooling equipment. The meaningful outcome is that objectionable datacenter hum is no longer perceptible or identifiable where neighboring communities experience it.

At the same time, acoustic mitigation must not compromise:

- cooling airflow;
- datacenter thermal safety;
- cooling performance;
- compute capacity;
- fan operating points;
- datacenter availability; or
- equipment reliability.

QuietEarth therefore investigates whether persistent tonal acoustic energy can be controlled close to the cooling\-system acoustic radiation path while leaving the required airflow path available.

---

# 3\. The QuietEarth Hypothesis

Cooling infrastructure requires large airflow paths.

Those openings can also become acoustic radiation paths through which fan tones and harmonics escape.

QuietEarth proposes an **Active Acoustic Aperture**:

1. Cooling airflow continues through an open path.
2. Persistent tonal acoustic energy approaches or reaches the aperture.
3. Reference sensing identifies dominant tonal components.
4. QuietEarth determines an acoustic control state.
5. Distributed control elements create a synchronized counteracting acoustic field.
6. Error microphones measure the residual tonal field.
7. QuietEarth searches for a lower\-residual control state.
8. QuietEarth verifies that state using repeated measurements.
9. QuietEarth maintains the state while acoustic conditions remain acceptable.
10. QuietEarth reacquires a better state when conditions change.

The Active Acoustic Aperture remains a proposed engineering architecture.

The hackathon did not physically validate a datacenter cooling aperture.

---

# 4\. Evidence Ladder

QuietEarth deliberately moved from simpler questions toward progressively more realistic evidence.

| Stage | Engineering Question | Hackathon Result |
| --- | --- | --- |
| Experiment 001 | Can a known tonal waveform be cancelled numerically under ideal conditions? | Yes |
| Experiment 002 | Does propagation delay alter the control state required for cancellation? | Yes |
| Jetson validation | Can the QuietEarth software stack execute successfully on edge hardware? | Yes |
| Physical acoustic acquisition | Can Jetson capture a real acoustic signal using a physical microphone? | Yes |
| Physical 440 Hz detection | Can QuietEarth identify a known tone after loudspeaker → air → microphone propagation? | Yes: 440.0 Hz |
| Physical 200 Hz detection | Is physical tone detection repeatable at another frequency? | Yes: 200.0 Hz |
| Experiment 003 | Can synchronized physical acoustic sources measurably alter the residual 200 Hz field? | Yes |
| Experiment 003 repeatability | Can a low\-residual physical state be reproduced? | Yes, three independent 45° trials |
| Experiment 004 | Can QuietEarth autonomously search physical measurements and select, verify, maintain, and reacquire a low\-residual tested state? | Yes, using recorded physical measurements |
| Active Acoustic Aperture | Has the complete airflow\-preserving datacenter aperture been physically validated? | No, this is the next validation stage |
| Datacenter/community outcome | Has QuietEarth demonstrated that nearby residents no longer hear datacenter hum? | No |

---

# 5\. Edge\-Compute Validation

QuietEarth was deployed to a Jetson Xavier edge device.

The environment used:

- isolated Python 3.12.14;
- QuietEarth virtual environment;
- existing Jetson software stack preserved;
- external Linux\-native storage for the development environment.

The complete automated test suite passed on Jetson.

At the earlier Jetson validation checkpoint:

**38 / 38 tests passed.**

Experiments 001 and 002 then executed successfully on the Jetson environment.

This established that the QuietEarth numerical and signal\-processing foundation could operate on representative edge hardware rather than only on the original development PC.

Later controller work expanded the complete repository test suite to:

**66 passing tests.**

---

# 6\. Physical Acoustic Acquisition

The next validation step deliberately left the purely numerical environment.

The physical signal chain was:

**digital test tone → physical loudspeaker → real air → physical microphone → USB audio → Jetson Xavier → QuietEarth**

A Jabra USB microphone was detected by the Jetson audio subsystem and used for acoustic acquisition.

A 440 Hz sine wave was played through a physical loudspeaker.

QuietEarth analyzed the microphone recording and returned dominant frequencies centered on:

**440.0 Hz**

A second physical experiment used a 200 Hz sine wave.

QuietEarth returned:

**200.0 Hz**

These measurements established that QuietEarth could process acoustic signals that had physically propagated through air rather than operating only on synthetic arrays generated inside software.

---

# 7\. Experiment 003: Physical Phase\-Controlled Tonal Attenuation

## 7.1 Objective

Determine whether synchronized physical acoustic control signals with controlled relative phase could produce measurable attenuation of a real 200 Hz acoustic tone at a fixed error\-microphone location.

## 7.2 Experimental Signal Chain

**Surface Laptop synchronized stereo playback**

↓

**Creative Inspire T2900 left and right loudspeakers**

↓

**physical acoustic propagation through air**

↓

**fixed Jabra USB error microphone**

↓

**Jetson Xavier acoustic acquisition**

↓

**QuietEarth** **compute\_fft()** **residual measurement**

## 7.3 Experimental Discipline

The experiment controlled key variables:

- one synchronized stereo playback clock;
- same 200 Hz target frequency;
- fixed microphone position;
- fixed loudspeaker positions;
- fixed playback level;
- fixed Creative amplifier level;
- fixed Jetson acquisition configuration;
- same QuietEarth FFT measurement path.

Relative phase between the two synchronized playback channels was varied.

## 7.4 Authoritative Experiment 003 Results

| Condition | Measured 200 Hz amplitude |
| --- | --- |
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

## 7.5 Repeatability

Three independent measurements were performed using the 45° control state.

Measured residual amplitudes:

1. **1.284177**
2. **0.844939**
3. **0.565633**

Arithmetic mean:

**0.898250**

Median:

**0.844939**

The three independently recorded trials all remained dramatically below the individual loudspeaker reference measurements.

## 7.6 Why Experiment 003 Matters

Experiment 003 did more than demonstrate a low number.

Changing the synchronized control state produced both attenuation and reinforcement.

For example:

- LEFT only: **58.652957**
- BOTH at 45°: approximately **0.9 mean residual**
- BOTH at 180°: **107.806039**

The physical acoustic field therefore responded strongly to the synchronized control state.

The experiment demonstrated a controlled acoustic variable capable of moving the measured physical system between:

- stronger residual tonal energy;
- progressively lower residual tonal energy; and
- strong reinforcement.

This is the physical control mechanism QuietEarth needs to exploit.

## 7.7 Measurement Qualification

Experiment 003 amplitudes are relative FFT amplitudes produced through the QuietEarth analysis path.

They are useful for controlled A/B comparison because the experimental geometry and acquisition configuration were held fixed.

They are **not** calibrated sound\-pressure\-level measurements.

Experiment 003 therefore does not establish:

- calibrated environmental dB reduction;
- whole\-room silence;
- outdoor attenuation;
- property\-boundary attenuation;
- residential attenuation;
- datacenter\-scale performance; or
- human imperceptibility.

---

# 8\. Experiment 004: Autonomous Tonal Control\-State Search

Experiment 003 demonstrated that a low\-residual physical acoustic state could exist.

Experiment 004 asked the next engineering question:

Can QuietEarth reason over acoustic measurements and autonomously determine which tested control state should be selected?

## 8.1 Controller Behavior

The Experiment 004 controller:

1. receives a target tonal frequency;
2. establishes a reference baseline;
3. evaluates candidate acoustic\-control states;
4. requests residual measurements through a provider\-independent interface;
5. aggregates repeated measurements;
6. selects the tested state with the lowest median residual amplitude;
7. independently verifies the selected state;
8. calculates relative reduction metrics;
9. enters **MAINTAIN** when verification satisfies configured criteria; and
10. requests **REACQUIRE** when a later residual exceeds a configured threshold.

## 8.2 Experiment 004 Results

Experiment 004 successfully selected:

**45°**

Verification trials:

- **1.284177**
- **0.844939**
- **0.565633**

Verification mean:

**0.898250**

Verification median:

**0.844939**

Reported amplitude reduction relative to the configured baseline:

**98.559426%**

Reported amplitude\-ratio reduction:

**36.829291 dB**

The dB value is an amplitude\-ratio calculation from uncalibrated FFT measurements. It is **not dB SPL**.

Controller state following verification:

**MAINTAIN**

When an elevated residual was introduced, the controller correctly requested:

**REACQUIRE**

## 8.3 Scientific Status Labels

Experiment 004 explicitly reports:

- **MEASUREMENT\_SOURCE: PHYSICAL\_RECORDINGS**
- **PHYSICAL\_ACOUSTIC\_ACQUISITION: TRUE**
- **AUTONOMOUS\_LIVE\_CONTROL: FALSE**
- **ACTIVE\_ACOUSTIC\_APERTURE\_VALIDATED: FALSE**
- **DATACENTER\_FIELD\_VALIDATED: FALSE**

These distinctions are deliberate.

The controller reasons autonomously over physical measurement data.

The controller does not yet perform live microphone\-to\-speaker closed\-loop physical control.

---

# 9\. The Active Acoustic Aperture Architecture

QuietEarth proposes moving the validated control mechanism to the acoustic escape path of cooling infrastructure.

Conceptually:

AI Datacenter Cooling Equipment

        \|

        \| cooling airflow

        \| persistent tonal acoustic energy

        v

Reference Acoustic Sensing

        \|

        v

QuietEarth Edge Controller

   DETECT

   SEARCH

   VERIFY

   MAINTAIN

   REACQUIRE

        \|

        \| phase / amplitude / delay /

        \| synchronized control state

        v

========================================

       ACTIVE ACOUSTIC APERTURE

 [Control]                [Control]

          OPEN AIRFLOW PATH

 [Control]                [Control]

========================================

        \|

        \| cooling airflow remains available

        \| residual acoustic field

        v

Error / Validation Microphones

        \|

        \+\-\-\-\-\-\- QuietEarth feedback

        \|

        v

Datacenter Boundary

        \|

        v

Surrounding Environment

        \|

        v

Nearby Community

The number, placement, type, frequency response, environmental protection, and acoustic power of future control elements remain engineering questions.

---

# 10\. What the Hackathon Proved

## PROVED

QuietEarth demonstrated:

- deterministic tonal\-signal simulation;
- spectral identification of target tones;
- idealized cancellation modeling;
- propagation\-delay modeling;
- phase compensation modeling;
- successful execution on Jetson Xavier;
- physical USB microphone acquisition;
- physical 440 Hz tone detection;
- physical 200 Hz tone detection;
- synchronized independent control of two acoustic sources;
- strong dependence of measured physical residual tone on relative control phase;
- repeatable low\-residual 200 Hz measurements at one fixed error\-microphone location;
- autonomous search of recorded physical measurement states;
- independent verification of a selected low\-residual state;
- MAINTAIN controller reasoning;
- REACQUIRE controller reasoning; and
- explicit separation of physical, simulated, and future live\-control evidence.

---

# 11\. What QuietEarth Has Architected

## ARCHITECTED

QuietEarth now has a proposed system architecture combining:

- reference acoustic sensing;
- edge tonal analysis;
- provider\-independent residual measurements;
- acoustic control\-state search;
- repeated verification;
- synchronized control sources;
- error\-microphone feedback;
- MAINTAIN behavior;
- REACQUIRE behavior;
- open cooling\-airflow path;
- distributed aperture control elements;
- multiple future validation sensors; and
- a validation path from physical laboratory evidence to community outcome.

The architecture keeps the long\-term goal unchanged:

Reduce objectionable tonal emissions without sacrificing the cooling infrastructure required to operate AI datacenters.

---

# 12\. What QuietEarth Has Not Yet Proved

## NOT YET VALIDATED

QuietEarth has not demonstrated:

- live closed\-loop microphone\-to\-speaker control;
- automatic live phase optimization;
- live amplitude optimization;
- live propagation\-delay adaptation;
- production acoustic actuators;
- an instrumented physical Active Acoustic Aperture;
- attenuation of a real cooling fan;
- control over multiple simultaneous fan tones;
- broadband cooling\-noise attenuation;
- attenuation over an extended spatial region;
- equivalent attenuation at multiple exterior microphones;
- preservation of airflow through physical hardware;
- acceptable static\-pressure impact;
- acceptable thermal impact;
- actuator power requirements;
- production fail\-open behavior;
- outdoor propagation performance;
- weather robustness;
- operational datacenter deployment;
- property\-boundary attenuation;
- half\-mile residential attenuation;
- human imperceptibility under quiet nighttime conditions;
- prevention of amplification at every unprotected location;
- regulatory compliance;
- patentability; or
- production readiness.

These are engineering and field\-validation milestones, not problems hidden by the hackathon narrative.

---

# 13\. Why the Result Matters

Before Experiment 003, QuietEarth had a plausible numerical hypothesis.

After Experiment 003, QuietEarth had physical evidence that synchronized acoustic control can create a repeatable low\-residual state for a real 200 Hz acoustic field at a fixed measurement point.

After Experiment 004, QuietEarth also had software capable of using measurement data to:

**SEARCH → VERIFY → MAINTAIN → REACQUIRE**

That progression changes the project from:

“Can anti\-noise theoretically cancel a tone?”

to:

“Can an edge\-controlled system discover and maintain acoustic states that suppress persistent tonal energy?”

The answer at the current experimental scale is sufficiently positive to justify the next level of engineering validation.

---

# 14\. Connection to the Datacenter Problem

Experiment 003 did not simulate a nearby resident.

Experiment 003 validated a building block.

The proposed translation is:

TODAY

Known 200 Hz tone

      ↓

Synchronized control sources

      ↓

Physical acoustic interference

      ↓

Error microphone

      ↓

Jetson \+ QuietEarth

      ↓

Low\-residual control state

NEXT

Real cooling fan

      ↓

Cooling outlet / airflow aperture

      ↓

Reference acoustic sensing

      ↓

QuietEarth edge controller

      ↓

Distributed aperture control elements

      ↓

Multiple error microphones

      ↓

Reduced escaping tonal field

      ↓

Datacenter boundary measurements

      ↓

Outdoor propagation measurements

      ↓

Representative residential measurements

QuietEarth must earn each arrow experimentally.

---

# 15\. Datacenter Validation Roadmap

## Stage 1: Source Characterization

Determine:

- which cooling assets produce objectionable tonal noise;
- which frequencies dominate;
- how tones change with equipment operating conditions;
- where acoustic energy leaves the cooling system;
- whether dominant radiation is through airflow openings, equipment panels, structures, or combinations of these paths.

## Stage 2: Controlled Fan Experiment

Use a real fixed\-speed fan and instrumented airflow path.

Measure:

- dominant tonal components;
- control OFF condition;
- control ON condition;
- repeatability;
- controller stability;
- unintended reinforcement.

## Stage 3: Physical Open\-Airflow Aperture

Construct a removable prototype around a real airflow opening.

Measure:

- tonal attenuation;
- airflow rate;
- static\-pressure change;
- temperature change;
- actuator power;
- loss\-of\-control behavior;
- physical fail\-open behavior.

## Stage 4: Spatial Validation

Use multiple microphones.

Map:

- attenuation zones;
- unchanged regions;
- reinforcement zones;
- optimal control\-source placement;
- error\-microphone requirements;
- number of required control channels.

## Stage 5: Outdoor Validation

Test:

- distance;
- direction;
- reflections;
- ground effects;
- wind;
- temperature variation;
- nighttime ambient conditions;
- atmospheric changes.

## Stage 6: Datacenter Pilot

Validate on representative cooling infrastructure without changing:

- fan operating points;
- cooling setpoints;
- workload;
- compute capacity;
- required cooling capacity; or
- datacenter safety behavior.

## Stage 7: Community\-Centered Validation

The final validation asks whether QuietEarth improves the human environment.

Evaluate whether:

- identifiable tonal hum is reduced at the datacenter boundary;
- identifiable tonal hum is reduced at representative nearby residences;
- ordinary field microphones can still capture an identifiable hum;
- residents can still perceive or identify the tonal component;
- another neighborhood receives increased acoustic energy;
- cooling and compute performance remain unchanged.

---

# 16\. Fail\-Safe Engineering Principles

QuietEarth must not:

- reduce compute capacity;
- modify workloads to reduce noise;
- require reduced fan speeds;
- require less cooling airflow;
- compromise thermal safety;
- interfere with datacenter reliability;
- require equipment at nearby residences;
- depend on community\-side sound masking;
- simply move objectionable noise elsewhere;
- generate unsafe acoustic output; or
- represent laboratory evidence as datacenter field validation.

A future physical Active Acoustic Aperture should be designed so loss of QuietEarth control does not obstruct required cooling airflow.

Datacenter cooling, thermal safety, and equipment reliability remain higher\-priority constraints than acoustic mitigation.

---

# 17\. Hackathon Outcome

The hackathon did not finish with a claim that QuietEarth has solved datacenter noise.

It finished with something more defensible:

1. The tonal\-control hypothesis works numerically.
2. Propagation changes the required control state.
3. QuietEarth runs on edge hardware.
4. QuietEarth detects physical acoustic signals.
5. Synchronized control state changes measurably affect a physical 200 Hz acoustic field.
6. A repeatable low\-residual physical state was observed.
7. QuietEarth can autonomously search physical measurement data and select and verify the lowest\-residual tested state.
8. QuietEarth has an engineering architecture for extending this capability toward airflow\-preserving datacenter acoustic control.
9. The remaining validation path is known and explicitly documented.

---

# 18\. The QuietEarth Story in One Sentence

**QuietEarth explores whether edge intelligence and synchronized acoustic control can reduce persistent tonal noise where it escapes AI datacenter cooling infrastructure, while keeping the airflow required for reliable compute open.**

---

# 19\. Final Vision

QuietEarth's final vision remains simple:

**AI datacenters should deliver valuable compute without asking neighboring communities to sacrifice peace and quiet.**

The hackathon established the first physical and computational evidence needed to make that vision worth pursuing.
