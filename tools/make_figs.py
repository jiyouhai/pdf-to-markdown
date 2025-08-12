import matplotlib.pyplot as plt
import numpy as np
from math import pi

# 总分（/60）
tools_ = ["TextIn","Reducto","Mathpix","Marker","Internal"]
totals = [47,41,52,38,33]
plt.figure()
plt.bar(tools_, totals)
plt.title("Equal-weight totals (/60)")
plt.ylabel("Score")
plt.tight_layout()
plt.savefig("report/src/img/scoreboard.png", dpi=200)
plt.close()

# 六维雷达
labels = ["Structure","Formatting","Special","Cleanliness","Ease","Automation"]
scores = {
 "TextIn":[8,9,7,8,7,8],
 "Reducto":[5,6,9,7,6,8],
 "Mathpix":[9,7,9,9,9,9],
 "Marker":[7,9,3,6,6,7],
 "Internal":[4,5,5,7,5,7],
}
angles = [n/float(len(labels))*2*pi for n in range(len(labels))]; angles += angles[:1]
fig = plt.figure()
ax = plt.subplot(111, polar=True)
ax.set_xticks(angles[:-1]); ax.set_xticklabels(labels)
ax.set_yticklabels([]); ax.set_title("Per-dimension scores")
for name, vals in scores.items():
    ax.plot(angles, vals+vals[:1], linewidth=1, label=name)
    ax.fill(angles, vals+vals[:1], alpha=0.05)
ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.10))
plt.tight_layout()
plt.savefig("report/src/img/radar.png", dpi=200, bbox_inches='tight')
plt.close()
