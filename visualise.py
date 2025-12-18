import matplotlib.pyplot as plt
import seaborn as sns

def plot_esg(yesterday, today):
    sns.set_style("whitegrid")
    plt.figure(figsize=(6,4))
    sns.lineplot(x=["Yesterday", "Today"], y=[yesterday, today], marker="o")
    plt.title("ESG Score Movement")
    plt.ylabel("ESG Score")
    return plt
