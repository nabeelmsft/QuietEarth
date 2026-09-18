# Experiment 003: Phase-Coherent Physical Tonal Attenuation

## Objective

Demonstrate that synchronized acoustic control signals with controlled relative phase can produce repeatable attenuation of a physical 200 Hz tonal signal at a fixed error-microphone location.

## Physical Signal Chain

Surface Laptop
→ synchronized stereo control signal
→ Creative Inspire T2900 left/right speakers
→ physical acoustic propagation through air
→ Jabra USB microphone
→ Jetson Xavier
→ QuietEarth spectral analysis using `compute_fft()`

## Test Signal

- Frequency: 200 Hz
- Waveform: sine
- Sample rate: 44.1 kHz
- Stereo output
- Left and right channels generated from the same playback clock
- Relative phase varied between channels

## Fixed Experimental Geometry

The Jabra microphone was positioned approximately midway between the two Creative satellite speakers.

The microphone, speakers, playback volume, Creative amplifier volume, and acquisition configuration remained fixed during the phase-comparison measurements.

The JBL speaker was not used during this experiment.

## Results

| Condition | Measured 200 Hz amplitude |
|---|---:|
| Left speaker only | 58.652957 |
| Right speaker only | 52.448952 |
| Both, 345° | 57.369749 |
| Both, 0° | 39.933457 |
| Both, 15° | 29.684351 |
| Both, 30° | 15.072868 |
| Both, 45°, Trial 1 | 1.284177 |
| Both, 45°, Trial 2 | 0.844939 |
| Both, 45°, Trial 3 | 0.565633 |
| Both, 180° | 107.806039 |

The reported amplitudes are relative experimental FFT amplitudes produced by the QuietEarth `compute_fft()` measurement path. They are suitable for controlled comparison within this experiment and are not calibrated dB SPL measurements.

## Repeatability

Three independent recordings were performed at the 45° control setting.

Measured residual amplitudes:

1. 1.284177
2. 0.844939
3. 0.565633

Average residual amplitude:

**0.898250**

Relative to the left-speaker-only reference amplitude of 58.652957, the average 45° result represents approximately **98.5% lower measured 200 Hz amplitude at the fixed microphone location**.

## Observations

The measured residual changed strongly as the relative phase between the two synchronized acoustic sources changed.

The progression toward 45° was:

- 345°: 57.369749
- 0°: 39.933457
- 15°: 29.684351
- 30°: 15.072868
- 45° Trial 1: 1.284177
- 45° Trial 2: 0.844939
- 45° Trial 3: 0.565633

At 180°, the measured amplitude increased to 107.806039.

The experiment therefore demonstrates that changing relative phase can move the physical acoustic system between strong attenuation and strong reinforcement at the measurement location.

## Engineering Conclusion

Experiment 003 demonstrates repeatable phase-controlled attenuation of a physical 200 Hz acoustic tone at a fixed error-microphone location.

The result was produced using:

- real loudspeakers,
- real acoustic propagation through air,
- a physical microphone,
- synchronized phase-controlled signals,
- Jetson edge hardware, and
- the QuietEarth measurement pipeline.

This advances QuietEarth beyond purely simulated waveform cancellation.

## What This Experiment Does NOT Prove

Experiment 003 does not yet demonstrate:

- whole-room cancellation,
- cancellation across an outdoor area,
- attenuation at residential distances,
- suppression of an operational datacenter cooling system,
- automatic closed-loop phase adaptation,
- multiple-frequency or broadband cancellation,
- preservation of cooling airflow,
- production-scale Active Acoustic Aperture performance, or
- field validation at an operational datacenter.

These are subsequent engineering and validation stages.

## QuietEarth Significance

Experiment 003 validates that synchronized phase control can produce repeatable attenuation at one fixed error-microphone location under the tested physical geometry.

The next engineering milestone is to replace manual phase selection with a closed-loop controller that automatically measures residual tonal energy and continuously adjusts control phase, amplitude, and delay to minimize it.

Longer term, this control mechanism is intended to become part of an airflow-preserving Active Acoustic Aperture positioned at datacenter acoustic emission paths.