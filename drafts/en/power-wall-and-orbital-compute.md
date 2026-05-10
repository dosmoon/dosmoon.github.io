# The Power Wall and Orbital Compute: AI Infrastructure's Next Leap

> **Version**: v2.1 (English edition)
> **Date**: May 2026

---

## Introduction

AI infrastructure in 2026 faces a plain fact: **Earth is running out**.

Not computation theory. Not algorithms. The physical limits of electricity, land, water, and grid lines are running out. When a single data center consumes the power of a mid-sized city, the next step has to be somewhere else. And "somewhere else" is no longer on Earth.

---

## I. The Ground Has Hit the Wall

### Where We Are Now

- **Colossus 1**: 220,000+ GPUs, 300+ MW, Memphis
- **Colossus 3**: under construction, scaling further
- AI data center power growth far outpaces grid capacity additions; the IEA now lists AI as a primary electricity consumer

### Three Physical Bottlenecks

1. **Power**: a single hyperscale data center routinely demands hundreds of megawatts to gigawatts — equivalent to a mid-sized nuclear plant. New capacity takes 3–5 years minimum.
2. **Cooling**: liquid cooling needs huge water volumes or closed-loop systems, infeasible in water-stressed regions; air cooling no longer works at high-density GPU racks.
3. **Land and grid**: high-voltage transmission, substations, land permitting — these timelines are often longer than building the data center itself.

### Short-Term Fixes Aren't Enough

- Restarting/expanding nuclear (Microsoft–Three Mile Island, Amazon–Talen, etc.)
- Self-built natural gas generation
- Reactivating retired coal plants

These are multi-year engineering projects, while model scale and inference demand follow quarterly curves. **The cadences don't match.**

---

## II. The Birth of Orbital Compute

### Key Events

- **February 2026**: xAI merged into SpaceX, forming SpaceXAI
- **May 6, 2026**: SpaceXAI leased the entire compute capacity of Colossus 1 to Anthropic, easing the explosive demand pressure on the Claude family
- The two parties simultaneously began exploring long-term cooperation on **orbital AI compute**

This isn't a random business headline. It reveals an underlying judgment: **the ground can no longer rescue AI's exponential compute curve. The next leap has to happen in orbit.**

---

## III. Why Space

Orbital compute sounds like science fiction, but every reason is solid.

### 1. 24-Hour Sunlight

In geostationary or appropriate sun-synchronous orbits, solar panels generate power continuously, almost without occlusion. Ground photovoltaics has a real-world utilization rate below 25% (night, clouds, latitude losses). **Space photovoltaics has at least 4× the energy density of ground.**

### 2. Vacuum Cooling Comes Free

The other half of a data center's cost is cooling. In vacuum, radiative cooling (Stefan-Boltzmann law) eliminates the need for water, cooling towers, or refrigerant pumps. Radiator surface area must be large, but no consumables are required.

### 3. Zero Land, Zero Grid, Zero Water

No land acquisition, no substations, no high-voltage lines, no water permits. The entire ground infrastructure stack disappears.

### 4. Starship's Inflection Point

Reusable hundred-tonne LEO capacity has driven cost-to-orbit to historic lows. When orbital insertion drops to the few-hundred-dollars-per-kilogram range, **the capex to deploy an orbital compute station approaches that of building a ground supercomputer** — but the operating cost structure is completely different.

---

## IV. Bypassing SBSP's Hardest Problem

Traditional **Space-Based Solar Power (SBSP)** has been stuck on one problem for decades: **how to transmit the power back to Earth?**

Microwave or laser downlink efficiency, safety, ground rectennas, regulation — none of these have ever been truly solved. Every SBSP plan, when it was proposed, fell at this step.

**Orbital compute eliminates this problem.**

Power isn't beamed back. **Compute results return as data.** A kilogram of data is much easier to transmit than a kilogram of power — laser communication links have already been validated on Starlink and lunar missions.

Coupling "space generation" with "space compute" means:

```
Solar panels → AI chips → Data downlink
(generation)  (orbital compute)  (laser / Ka-band)
```

This is why orbital compute may mature before SBSP — it doesn't need to solve SBSP's hardest step.

---

## V. Engineering Challenges

Don't romanticize this. The hard problems orbital compute faces:

### 1. Radiation Hardening

Cosmic rays and solar particle events trigger single-event upsets (SEU), latch-ups, and dose accumulation. Commercial GPUs can't go directly to space; they need hardware-level redundancy, full-stack ECC coverage, or specialized processes (SOI, rad-hard design).

### 2. Heat Dissipation

In vacuum the only option is radiative cooling. A 1MW compute station needs a radiator surface area of **thousands of square meters** (depending on cold-side temperature). This is the real engineering bottleneck — possibly harder than power itself.

### 3. On-Orbit Maintenance

Even with GPU failure rates as low as 0.1%/year, 220,000 cards mean hundreds of replacements per day. This requires modular on-orbit replacement capacity coordinated with Starship/Dragon-class vehicles, or designs that can run with redundant degradation.

### 4. Up/Downlink Bandwidth

Laser communication capacity determines what fraction of workloads orbital compute can carry. **Likely division of labor**:
- Training: stays on the ground, data-intensive
- Inference: moves to orbit, compute-intensive with small output data

### 5. Policy and Orbital Resources

Low Earth orbit is already crowded; Kessler syndrome risk is rising; international regulation is immature; spectrum allocation is contested.

---

## VI. Timeline

| Phase | Time | Scale | Form |
|---|---|---|---|
| Demo | 2027–2028 | kW–MW | Hosted on Starlink V3 or dedicated platforms; single-satellite AI inference experiments |
| Transition | 2029–2031 | Hundreds of MW | Dedicated orbital compute stations, primarily inference |
| Scale | 2032+ | GW class | Orbital clusters comparable to ground Colossus |

The biggest uncertainty comes from **engineering progress on heat dissipation and on-orbit maintenance**, followed by the commercialization cost of laser communication bandwidth.

---

## VII. Conclusion

AI is, for the first time, forcing humanity to move infrastructure off Earth. Not for romance — because grid power, river water, and land have become the ceiling on the compute curve.

In the twentieth century we used oil to move industry to sea and underground.
In the twenty-first, AI will move computation to the sky.

Power is no longer the issue. **Heat dissipation and bandwidth** are the new bottlenecks. This is the fundamental driver pushing industrial infrastructure from two dimensions (the surface) into three (orbit).

---

*Next: "Token Processor and 3D Printing: Rebuilding the Industrial Stack" — discussing how the digital and physical sides are simultaneously being redefined.*
