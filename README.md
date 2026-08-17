# CVD Oxide Thickness Process Control
# SPC Dashboard — CVD Oxide Thickness Process Control

##  Dashboard

<img width="1885" height="943" alt="SPC-Thickness (2)" src="https://github.com/user-attachments/assets/d1c4d2d1-e9aa-4818-a50f-1f1c4da7c464" />



---

## Overview

This project simulates a **CVD oxide thin-film deposition process** and applies Statistical Process Control (SPC) to monitor wafer thickness and identify abnormal process behavior.

The simulated process targets an oxide thickness of **100 nm**, with specification limits of **95–105 nm**. Data are generated for **150 production lots with 5 wafers per lot**.

The analysis implements **X̄-R control charts, Western Electric rules, process capability analysis (Cp/Cpk), and distribution analysis** to distinguish normal process variation from potential special-cause events.

The objective is to demonstrate how a engineer can use manufacturing data to **monitor process stability, detect shifts, evaluate capability, and recommend corrective actions**.

---

##  Key Findings

- The **X̄ control chart** was used to monitor shifts in the average oxide thickness across production lots.
- The **R chart** was used to monitor within-lot variation and identify changes in process consistency.
- **Western Electric rules** were implemented to detect potential special-cause variation that may not necessarily exceed the control limits.
- **Cp and Cpk** were calculated to evaluate whether the simulated process can consistently meet the specified thickness requirements.
- The analysis demonstrates that **statistical control and specification compliance are different concepts**: a process can be stable while still being incapable of meeting customer specifications.

> **Note:** The process data in this project are simulated and are not from an actual semiconductor fabrication facility.

---

##  Recommendations

Based on the SPC signals, a engineer could investigate:

1. **Process parameter drift**  
   Check deposition temperature, chamber pressure, and other CVD parameters if a sustained shift in mean thickness is detected.

2. **Increasing process variation**  
   Investigate equipment condition, wafer-to-wafer variation, chamber uniformity, and measurement-system issues when the R chart indicates increased variation.

3. **Special-cause events**  
   Lots triggering Western Electric rules should be investigated for equipment events, maintenance activity, contamination, recipe changes, or other assignable causes.

4. **Process capability improvement**  
   If Cp/Cpk indicates insufficient capability, reduce process variation and/or recenter the process toward the target thickness.

---

##  Methods

### Process Simulation

- Target thickness: **100 nm**
- Lower Specification Limit (LSL): **95 nm**
- Upper Specification Limit (USL): **105 nm**
- Lots: **150**
- Wafers per lot: **5**
- Simulated thickness distribution: Normal distribution

### Statistical Methods

- Subgroup mean calculation
- Subgroup range calculation
- Grand mean
- Average range
- X̄ control limits
- R control limits
- Process standard deviation estimation
- Cp and Cpk
- Western Electric Rule 1
- Western Electric Rule 4
- Histogram and normal distribution comparison

---

##  Control Charts

### X̄ Chart

The X̄ chart monitors changes in the **average oxide thickness of each production lot**.

It helps identify:

- Sudden process shifts
- Sustained changes in process mean
- Potential special-cause variation

### R Chart

The R chart monitors **within-lot variation**.

It helps identify:

- Increasing process variability
- Loss of process consistency
- Potential equipment or process instability

---

##  Engineering Interpretation

The purpose of the project is to calculate SPC limits and
get experience of the analysis that follows the engineering workflow:

```text
Manufacturing Process
        ↓
Thickness Measurements
        ↓
Subgroup Formation
        ↓
SPC Monitoring
        ↓
Detect Abnormal Behavior
        ↓
Interpret Possible Cause
        ↓
Recommend Corrective Action
