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

## Safe MVP

The initial MVP is a software-only simulation.

It models:

- a synthetic cooling-fan tone;
- configurable harmonics;
- an idealized acoustic outlet;
- a simulated active-control signal;
- control OFF and ON conditions; and
- residual tonal energy outside the aperture.

The MVP will produce transparent, reproducible metrics while clearly labeling every result as simulated.

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

**Stage:** Research and simulation  
**Production-ready:** No  
**Field-validated:** No  
**Patent determination:** Not completed

## Vision

QuietEarth’s vision is simple:

> AI datacenters should deliver valuable compute without asking neighboring communities to sacrifice peace and quiet.
