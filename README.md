# QuietEarth

**Making AI infrastructure a better neighbor.**

QuietEarth is a Microsoft Hackathon 2026 research and proof-of-concept project exploring whether an **Active Acoustic Aperture** can suppress persistent tonal noise emitted through AI datacenter cooling outlets while preserving airflow, cooling performance, compute capacity, and datacenter reliability.

## The problem

Communities near large AI datacenters may experience persistent tonal humming or droning from continuously operating cooling infrastructure. Even when the overall sound level is relatively low, a stable and identifiable tone can remain noticeable, especially during quiet nighttime conditions.

The human outcome matters more than a headline decibel value:

> QuietEarth succeeds only when residents can no longer perceive or identify the datacenter hum under representative worst-case listening conditions.

## Project hypothesis

Cooling equipment requires large, continuously open airflow paths. These openings can also become acoustic radiation paths through which fan tones and harmonics escape.

QuietEarth investigates a retrofit device called an **Active Acoustic Aperture**:

1. Cooling airflow passes through an open aperture.
2. Tonal acoustic energy reaches the aperture.
3. Distributed acoustic control elements create a counteracting pressure field at the aperture.
4. The dominant tonal components are reduced before they radiate into the surrounding environment.
5. Required airflow remains available.
6. If the device loses power, it fails open and does not obstruct cooling.

This is a research hypothesis, not a claim of proven field performance.

## Project progress

### Demonstrated

- QuietEarth runs on Jetson Xavier.
- Existing automated tests pass on the edge device.
- Real 440 Hz and 200 Hz acoustic tones were captured and identified.
- Experiment 003 demonstrated repeatable phase-controlled attenuation of a
  physical 200 Hz tone at a fixed error-microphone location.
- The controller can autonomously search recorded or simulated measurement
  landscapes and select the lowest-residual tested control state.

### Not yet demonstrated

- Live closed-loop microphone and speaker control
- Whole-room or broad outdoor cancellation
- Multiple-microphone quiet-zone control
- An airflow-preserving physical aperture
- Airflow, static-pressure, and thermal validation
- Real cooling-fan attenuation
- Operational datacenter validation
- Half-mile residential attenuation
- Human imperceptibility under quiet nighttime conditions
- Prevention of amplification at all unprotected locations
- Patentability or production readiness

The intended engineering progression is:

```text
Experiment 003 physical proof
→ Controller search and state maintenance
→ Live microphone measurement provider
→ Live synchronized control output
→ Instrumented open-aperture prototype
→ Fixed-speed cooling-fan experiment
→ Multiple exterior error microphones
→ Airflow and thermal validation
→ Outdoor spatial mapping
→ Datacenter pilot
→ Independent residential validation
```

## Non-negotiable constraints

QuietEarth must not:

- reduce compute capacity;
- modify workloads;
- change cooling setpoints;
- change fan operating points;
- interfere with datacenter reliability;
- require devices at residences;
- require community-side sound masking;
- relocate objectionable sound to another community;
- create unsafe sound-pressure levels; or
- represent simulated results as real-world validation.

All mitigation equipment is intended to remain within the datacenter boundary.

## Initial MVP: Software simulation

This was QuietEarth's starting validation stage. The project has since progressed beyond the initial software-only MVP into physical single-point acoustic validation and a recorded-measurement controller MVP. See Project progress, Experiment 003, and Experiment 004.

The initial MVP is a software-only simulation.

It models:

- a synthetic cooling-fan tone;
- configurable harmonics;
- an idealized acoustic outlet;
- a simulated active-control signal;
- control OFF and ON conditions; and
- residual tonal energy outside the aperture.

The MVP produced transparent, reproducible metrics while clearly labeling every result as simulated.

### What the MVP can demonstrate

- A repeatable tonal-noise simulation.
- Spectral identification of a fundamental tone and its harmonics.
- The theoretical effect of an anti-phase control signal.
- A proposed measurement framework for evaluating the aperture.
- The architecture of a later tabletop experiment.

### What the MVP cannot demonstrate

- Elimination of noise at an operating datacenter.
- Industrial-scale performance.
- Preservation of airflow in physical hardware.
- Stability under outdoor weather conditions.
- Human imperceptibility at a residence half a mile away.
- Patentability, regulatory compliance, or production readiness.

## Conceptual architecture

```text
Synthetic cooling-fan signal
             |
             v
    Spectral analysis
             |
             v
  Tonal-control simulator
             |
             v
Idealized acoustic aperture
             |
             v
   Simulated exterior field
             |
             v
 Impact and safety metrics
```

A future tabletop prototype may add:

```text
Fixed-speed fan
      |
      v
Instrumented test duct
      |
      v
Active Acoustic Aperture
      |
      +--> Airflow and pressure sensors
      |
      +--> Exterior measurement microphones
```

## Proposed components

### Software

- Synthetic signal generator
- Narrowband spectral analyzer
- Simplified aperture model
- Tonal-control simulator
- Impact metrics
- FastAPI interface
- Automated tests

### Future tabletop hardware

Hardware is deliberately outside the first implementation pull request.

A later experiment may use:

- a small test duct;
- a fixed-speed axial fan;
- a removable aperture frame;
- low-frequency control transducers;
- measurement microphones;
- a multichannel audio interface;
- a deterministic controller;
- an anemometer;
- differential-pressure sensors;
- temperature sensors;
- power amplifiers; and
- an emergency cutoff.

No hardware test should proceed without an acoustic engineer reviewing the design and its safety boundaries.

## Success metrics

The project separates simulation, laboratory, and field success.

### Simulation success

- Correctly identify configured fundamental tones and harmonics.
- Produce deterministic and reproducible results.
- Show calculated reduction in targeted tonal components.
- Report residual energy and all assumptions.
- Avoid claiming real-world attenuation.

### Tabletop success

A later physical prototype would compare control OFF and ON while holding the source and fan operation constant.

It should measure:

- reduction of dominant tonal peaks;
- reduction across multiple exterior microphone positions;
- absence of material amplification at unprotected positions;
- airflow change;
- static-pressure change;
- temperature change;
- controller stability;
- actuator power; and
- fail-open behavior.

### Long-term field success

Field success requires independent validation under quiet nighttime conditions.

The intended outcome is:

- residents cannot perceive or identify the datacenter hum;
- ordinary broadcast microphones cannot capture an identifiable hum;
- sensitive instruments may detect residual energy;
- cooling and compute performance remain unchanged; and
- no neighboring location experiences displaced or amplified noise.

## Running locally

QuietEarth requires Python 3.12. Create a virtual environment and install the
project dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

Start the API:

```bash
uvicorn src.api.main:app --reload
```

The initial implementation is intentionally small:

- `src/acoustic_model/signal_generator.py` creates deterministic synthetic
  tones and harmonics.
- `src/acoustic_model/spectral_analysis.py` computes one-sided spectra and
  identifies dominant frequencies.
- `src/acoustic_model/metrics.py` calculates simulated RMS reduction.
- `src/api/main.py` exposes health and simulation endpoints.

No user interface or physical-control integration is included.

## Physical acoustic validation: Experiment 003

Experiment 003 moved QuietEarth beyond simulation into controlled physical
acoustic validation.

The experiment used two Creative Inspire T2900 loudspeakers driven by
synchronized stereo signals from the same playback clock. A Jabra USB
microphone served as the fixed error-measurement microphone, and Jetson Xavier
captured the physical acoustic signal. QuietEarth measured the residual
200 Hz component using the existing `compute_fft()` analysis path.

The experimentally measured 200 Hz amplitudes included:

| Control condition | Measured 200 Hz amplitude |
| --- | ---: |
| Left speaker only | 58.652957 |
| Right speaker only | 52.448952 |
| Both channels, 345 degrees | 57.369749 |
| Both channels, 0 degrees | 39.933457 |
| Both channels, 15 degrees | 29.684351 |
| Both channels, 30 degrees | 15.072868 |
| Both channels, 45 degrees, trial 1 | 1.284177 |
| Both channels, 45 degrees, trial 2 | 0.844939 |
| Both channels, 45 degrees, trial 3 | 0.565633 |
| Both channels, 180 degrees | 107.806039 |

The three independent 45-degree verification trials produced measured residual
amplitudes of `1.284177`, `0.844939`, and `0.565633`, with an arithmetic mean
of approximately `0.898250`.

These measurements demonstrate repeatable phase-controlled attenuation of a
physical 200 Hz acoustic tone at one fixed error-microphone location. The
measurements are uncalibrated FFT amplitude values and must not be represented
as calibrated dB SPL.

Changing the relative control phase also produced strong reinforcement at
180 degrees, demonstrating that the measured acoustic field was strongly
dependent on the synchronized control state.

Experiment 003 does not demonstrate whole-room cancellation, outdoor
attenuation, an airflow-preserving Active Acoustic Aperture, real cooling-fan
attenuation, datacenter-scale performance, or residential imperceptibility.

The canonical engineering validation record for the experiment is maintained
in the Experiment 003 documentation, and the machine-readable measurements
used by the controller are stored in
`validation_data/experiment_003_physical_tonal_attenuation.json`.

Experiment 003 serves as the first physical regression case for the QuietEarth
controller. Experiment 004 builds on this evidence by autonomously searching
the recorded measurement landscape, selecting the lowest-residual tested
control state, verifying that state using repeated measurements, and deciding
when reacquisition is required.

## Autonomous controller experiment

Experiment 004 applies the same provider-independent controller search to the
recorded Experiment 003 physical measurements:

```bash
python -m experiments.experiment_004_controller_phase_search
```

The controller searches candidate acoustic-control states using measured residual tonal amplitude. In Experiment 004, the control variable is relative phase; future live control can extend the same architecture to phase, amplitude, delay, and other control parameters,
uses deterministic variation/trial-count/phase tie-breaking, verifies the
selected state with repeated measurements, calculates finite amplitude-ratio
metrics, enters a conceptual `MAINTAIN` state when the configured reduction is
met, and models a threshold-based reacquisition decision.

The machine-readable physical measurements are stored in
`validation_data/experiment_003_physical_tonal_attenuation.json`. The provider
does not interpolate unmeasured phases. A simulation provider uses the same
controller interface, and a future live provider can measure a fixed audio
window through the existing `compute_fft()` path without changing the search
algorithm.

Experiment 004 does not capture microphone audio or control speakers,
amplifiers, fans, cooling equipment, or datacenter assets. Its physical inputs
are recorded single-location measurements, not calibrated dB SPL values. It
does not establish whole-room, open-aperture, outdoor, residential, airflow,
thermal, or datacenter-field performance.

## Example simulation request

```json
{
  "fundamental_hz": 120,
  "harmonics": 3
}
```

The simulation response identifies the dominant frequencies:

```json
{
  "dominant_frequencies": [120, 240, 360],
  "simulation": true
}
```

## Ideal cancellation experiment

Experiment 001 demonstrates idealized waveform superposition for a known pure
tone:

```bash
python -m experiments.experiment_001_ideal_cancellation
```

The experiment generates a 120 Hz primary tone and an equal-amplitude control
tone with a 180-degree phase offset. It reports RMS, energy, residual energy
ratio, and reduction when the result is above the floating-point numerical
floor.

This deterministic simulation does not model propagation delay, speaker or
microphone transfer functions, reflections, airflow, wind, actuator limits,
changing acoustic paths, real-time latency, or physical Active Acoustic
Aperture behavior. Mathematical waveform cancellation does not prove
datacenter noise reduction.

## Propagation delay experiment

Experiment 002 isolates propagation delay and compares equal paths, mismatched
paths without compensation, and the same mismatch with calculated phase
compensation:

```bash
python -m experiments.experiment_002_propagation_delay
```

The model rounds travel time to the nearest whole sample, delays by zero
padding, truncates samples shifted beyond the observation window, and never
wraps delayed samples to the beginning. The speed of sound defaults to 343
m/s but is configurable; 343 m/s is not treated as universally exact.

This experiment only demonstrates that propagation delay changes the phase
relationship between simulated primary and control signals. It excludes
speaker and microphone characteristics, reflections, airflow, wind,
atmospheric conditions, environmental geometry, processing and actuator
latency, multiple sources, spatial cancellation, and physical Active Acoustic
Aperture behavior. It does not prove physical or field attenuation.

## Research questions

1. What tonal frequencies dominate objectionable cooling-fan noise?
2. At which cooling-system surfaces or openings does that energy radiate?
3. Can an aperture-mounted system reduce the tones without restricting airflow?
4. What transducer architecture can produce sufficient low-frequency output?
5. How can the controller avoid amplifying sound in another direction?
6. How should the system fail safely when power or control is unavailable?
7. Can the approach scale from one outlet to a hyperscale cooling installation?
8. What evidence would be required to prove human imperceptibility at nearby residences?

## Responsible engineering

QuietEarth prioritizes:

- human wellbeing;
- datacenter safety;
- transparent measurement;
- independent validation;
- privacy;
- fail-safe behavior;
- environmental responsibility; and
- honest communication of limitations.

The repository must not contain confidential datacenter information, resident recordings, personal information, security-sensitive facility details, or unapproved operational telemetry.

## Repository status

**Stage:** Research, physical single-point proof, and recorded-data controller MVP
**Production-ready:** No  
**Field-validated:** No  
**Patent determination:** Not completed

## Vision

QuietEarth’s vision is simple:

> AI datacenters should deliver valuable compute without asking neighboring communities to sacrifice peace and quiet.
