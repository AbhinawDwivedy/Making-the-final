# import os
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns

# # ======================================================
# # CONFIG & PATHS
# # ======================================================
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# INPUT_CSV = os.path.join(BASE_DIR, "full_matrix_metrics.csv")
# OUTPUT_DIR = os.path.join(BASE_DIR, "analytics_output")

# class URLAnalytics:
#     def __init__(self, df):
#         self.df = df
#         self.output_dir = OUTPUT_DIR
#         os.makedirs(self.output_dir, exist_ok=True)
        
#         # Define "Pass" as a Score >= 4 (You can change this to == 5 for stricter pass)
#         self.df['passed'] = self.df['url_score'] >= 4

#     def run_full_analysis(self):
#         print(f"\n📈 Generating Graphs in: '{self.output_dir}'")
        
#         # Set the style
#         sns.set_theme(style="whitegrid")
        
#         # 1. THE MANDATORY GRAPH: Writer vs Judge Comparison
#         print("   1. Creating Mandatory Writer vs Judge Bar Chart...")
#         self.plot_writer_vs_judge_bar()

#         # 2. Strictness Distribution (Box Plot)
#         print("   2. Creating Judge Strictness Box Plot...")
#         self.plot_judge_strictness()
        
#         # 3. Simple Matrix Heatmap (Overview)
#         print("   3. Creating Heatmap...")
#         self.plot_matrix_heatmap()

#         print(f"✅ Analytics Complete! Check the '{os.path.basename(self.output_dir)}' folder.")

#     def plot_writer_vs_judge_bar(self):
#         """
#         MANDATORY GRAPH:
#         X-Axis: Writer Model (Mini vs 4.1)
#         Y-Axis: Pass Rate %
#         Hue (Colors): Judge Model (Mini vs 4.1)
#         """
#         plt.figure(figsize=(10, 6))
        
#         # Aggregate pass rate by Writer & Judge
#         data = self.df.groupby(['writer_model', 'judge_model'])['passed'].mean().reset_index()
#         data['passed'] = data['passed'] * 100  # Convert to percentage

#         # Plot
#         ax = sns.barplot(
#             data=data,
#             x="writer_model",
#             y="passed",
#             hue="judge_model",
#             palette="viridis"
#         )

#         # Labels
#         plt.title("Writer Performance vs Judge Evaluation (Pass Rate %)", fontsize=15, fontweight='bold')
#         plt.xlabel("Writer Model (Who wrote the email?)", fontsize=12)
#         plt.ylabel("Pass Rate (%)", fontsize=12)
#         plt.ylim(0, 115) # Extra space for labels
#         plt.legend(title="Judge Model")

#         # Add percentage numbers on top of bars
#         for container in ax.containers:
#             ax.bar_label(container, fmt='%.1f%%', padding=3, fontweight='bold')

#         plt.tight_layout()
#         plt.savefig(os.path.join(self.output_dir, "1_Writer_vs_Judge_Comparison.png"))
#         plt.close()

#     def plot_judge_strictness(self):
#         """
#         Shows the range of scores given by each judge.
#         """
#         plt.figure(figsize=(8, 6))
#         sns.boxplot(data=self.df, x="judge_model", y="url_score", palette="Set2")
#         plt.title("Judge Strictness: Score Distribution (1-5)", fontsize=14)
#         plt.ylabel("Score Given")
#         plt.xlabel("Judge Model")
#         plt.tight_layout()
#         plt.savefig(os.path.join(self.output_dir, "2_Judge_Strictness.png"))
#         plt.close()

#     def plot_matrix_heatmap(self):
#         """
#         2x2 Matrix showing the exact numbers in a grid.
#         """
#         pivot = self.df.pivot_table(
#             index="writer_model", 
#             columns="judge_model", 
#             values="passed", 
#             aggfunc="mean"
#         ) * 100
        
#         plt.figure(figsize=(8, 6))
#         sns.heatmap(pivot, annot=True, cmap="Blues", fmt=".1f", vmin=0, vmax=100)
#         plt.title("Pass Rate Heatmap (%)")
#         plt.ylabel("Writer")
#         plt.xlabel("Judge")
#         plt.tight_layout()
#         plt.savefig(os.path.join(self.output_dir, "3_Matrix_Heatmap.png"))
#         plt.close()

# # ======================================================
# # MAIN
# # ======================================================
# def main():
#     if not os.path.exists(INPUT_CSV):
#         print(f"❌ Error: '{INPUT_CSV}' not found.")
#         print("💡 You must run 'python url_evaluate.py' first.")
#         return

#     print("🚀 Starting Visual Analytics...")
#     try:
#         df = pd.read_csv(INPUT_CSV)
#         analytics = URLAnalytics(df)
#         analytics.run_full_analysis()
#     except Exception as e:
#         print(f"❌ Error reading CSV or generating graphs: {e}")

# if __name__ == "__main__":
#     main()
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ======================================================
# CONFIG & PATHS
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "full_matrix_metrics.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "analytics_output")

class URLAnalytics:
    def __init__(self, df):
        self.df = df
        self.output_dir = OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        
        # ---------------------------------------------------------
        # DEFINITION OF "PASS"
        # ---------------------------------------------------------
        # Strict URL preservation usually requires a 5 (Exact Match).
        # We allow 4 (Minor whitespace formatting) as a pass too.
        self.df['passed'] = self.df['url_score'] >= 4

    def run_full_analysis(self):
        print(f"\n📈 Generating Graphs in: '{self.output_dir}'")
        
        # Set the visual style
        sns.set_theme(style="whitegrid")
        
        # 1. Comparison Bar Chart
        print("   1. Creating Writer vs Judge Bar Chart...")
        self.plot_writer_vs_judge_bar()

        # 2. Strictness Box Plot
        print("   2. Creating Judge Strictness Box Plot...")
        self.plot_judge_strictness()
        
        # 3. Matrix Heatmap
        print("   3. Creating 2x2 Heatmap...")
        self.plot_matrix_heatmap()

        print(f"✅ Analytics Complete! Check the '{os.path.basename(self.output_dir)}' folder.")

    def plot_writer_vs_judge_bar(self):
        """
        X-Axis: Writer Model
        Y-Axis: Pass Rate % (Score >= 4)
        Hue: Judge Model
        """
        plt.figure(figsize=(10, 6))
        
        # Aggregate pass rate
        data = self.df.groupby(['writer_model', 'judge_model'])['passed'].mean().reset_index()
        data['passed'] = data['passed'] * 100  # Convert to percentage

        # Plot
        ax = sns.barplot(
            data=data,
            x="writer_model",
            y="passed",
            hue="judge_model",
            palette="viridis"
        )

        plt.title("URL Preservation Success Rate by Writer & Judge", fontsize=14, fontweight='bold')
        plt.xlabel("Writer Model", fontsize=12)
        plt.ylabel("Pass Rate (%)", fontsize=12)
        plt.ylim(0, 115) 
        plt.legend(title="Judge Model")

        # Add labels
        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f%%', padding=3, fontweight='bold')

        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "1_Writer_vs_Judge_Comparison.png"))
        plt.close()

    def plot_judge_strictness(self):
        """
        Shows the distribution of scores (0-5) given by each judge.
        Helps identify if one judge is harsher than the other.
        """
        plt.figure(figsize=(8, 6))
        
        # FIXED: Added hue and legend=False to fix Future Warning
        sns.boxplot(
            data=self.df, 
            x="judge_model", 
            y="url_score", 
            hue="judge_model", 
            legend=False, 
            palette="Set2"
        )
        
        plt.title("Judge Strictness: Score Distribution", fontsize=14)
        plt.ylabel("URL Score Given (0-5)")
        plt.xlabel("Judge Model")
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "2_Judge_Strictness.png"))
        plt.close()

    def plot_matrix_heatmap(self):
        """
        A 2x2 Grid showing the exact pass rate numbers.
        """
        # Create Pivot Table
        pivot = self.df.pivot_table(
            index="writer_model", 
            columns="judge_model", 
            values="passed", 
            aggfunc="mean"
        ) * 100
        
        plt.figure(figsize=(8, 6))
        
        # FIXED: Changed fmt=".1f%%" to fmt=".1f" to avoid formatting errors
        sns.heatmap(
            pivot, 
            annot=True, 
            cmap="Blues", 
            fmt=".1f", 
            vmin=0, 
            vmax=100, 
            annot_kws={"size": 14}
        )
        
        plt.title("Pass Rate Matrix Heatmap (%)", fontsize=14)
        plt.ylabel("Writer Model")
        plt.xlabel("Judge Model")
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, "3_Matrix_Heatmap.png"))
        plt.close()

# ======================================================
# MAIN
# ======================================================
def main():
    if not os.path.exists(INPUT_CSV):
        print(f"❌ Error: '{INPUT_CSV}' not found.")
        print("💡 You must run 'python url_evaluate.py' first to generate the data.")
        return

    print("🚀 Starting Visual Analytics...")
    try:
        df = pd.read_csv(INPUT_CSV)
        if df.empty:
            print("❌ Error: The CSV file is empty.")
            return
            
        analytics = URLAnalytics(df)
        analytics.run_full_analysis()
    except Exception as e:
        print(f"❌ Error reading CSV or generating graphs: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()