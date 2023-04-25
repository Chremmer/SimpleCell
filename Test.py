# importing pandas library
import pandas as pd
# importing matplotlib library
import matplotlib.pyplot as plt

# creating dataframe
df = pd.DataFrame({
    'Age': [45, 38, 90, 60, 40, 50, 2, 32, 8, 15, 27, 69, 73, 55]
})

# plotting a histogram
plt.plot(df["Age"])
plt.show()
