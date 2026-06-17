"""
ML Pipeline GUI — main entry point.
Run:  python -m gui.app
"""

import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# ── colour tokens ──────────────────────────────────────────────────────────────
BG        = "#0f1117"   # near-black canvas
PANEL     = "#1a1d27"   # card surface
BORDER    = "#2a2d3a"   # subtle rule
ACCENT    = "#5c6cfa"   # indigo primary
ACCENT2   = "#a78bfa"   # violet secondary
SUCCESS   = "#34d399"   # green
WARN      = "#fbbf24"   # amber
DANGER    = "#f87171"   # red
TEXT      = "#e2e8f0"   # primary text
MUTED     = "#64748b"   # secondary text
MONO      = "Courier New"
SANS      = "Segoe UI" if sys.platform == "win32" else "SF Pro Display" if sys.platform == "darwin" else "Ubuntu"

STAGES = ["Import", "Schema", "EDA", "Clean", "Features", "Models", "Train", "Results", "Export"]

# ── helpers ────────────────────────────────────────────────────────────────────
def styled_frame(parent, **kw):
    kw.setdefault("bg", PANEL)
    kw.setdefault("relief", "flat")
    return tk.Frame(parent, **kw)

def label(parent, text, size=10, weight="normal", color=TEXT, **kw):
    kw.update(bg=kw.get("bg", PANEL), fg=color,
              font=(SANS, size, weight), text=text)
    return tk.Label(parent, **kw)

def button(parent, text, cmd, accent=True, small=False, **kw):
    bg   = ACCENT if accent else BORDER
    fg   = "#ffffff"
    size = 9 if small else 10
    b = tk.Button(parent, text=text, command=cmd,
                  bg=bg, fg=fg, activebackground=ACCENT2,
                  activeforeground="#fff", relief="flat",
                  font=(SANS, size, "bold"),
                  padx=14, pady=6 if not small else 4,
                  cursor="hand2", bd=0, **kw)
    b.bind("<Enter>", lambda e: b.config(bg=ACCENT2))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b

def scrolled_text(parent, height=12, **kw):
    frame = tk.Frame(parent, bg=PANEL)
    sb    = tk.Scrollbar(frame, bg=BORDER, troughcolor=BG)
    t     = tk.Text(frame, height=height, bg=BG, fg=TEXT,
                    font=(MONO, 9), relief="flat", bd=0,
                    yscrollcommand=sb.set, wrap="none",
                    insertbackground=ACCENT, **kw)
    sb.config(command=t.yview)
    sb.pack(side="right", fill="y")
    t.pack(side="left", fill="both", expand=True)
    return frame, t

def pill(parent, text, color=ACCENT):
    f = tk.Frame(parent, bg=color, padx=8, pady=2)
    tk.Label(f, text=text, bg=color, fg="#fff",
             font=(SANS, 8, "bold")).pack()
    return f


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
class Sidebar(tk.Frame):
    def __init__(self, master, on_select):
        super().__init__(master, bg=PANEL, width=190)
        self.pack_propagate(False)
        self.on_select   = on_select
        self.btn_map     = {}
        self.active      = None

        # logo
        tk.Label(self, text="⬡ ML Pipeline", bg=PANEL, fg=ACCENT,
                 font=(SANS, 13, "bold"), pady=22).pack(fill="x", padx=18)
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=18)

        # nav items
        tk.Label(self, text="PIPELINE", bg=PANEL, fg=MUTED,
                 font=(SANS, 7, "bold"), pady=10).pack(fill="x", padx=18)

        icons = ["⬆", "🗂", "📊", "🧹", "⚙", "🤖", "🏋", "📈", "📦"]
        for icon, stage in zip(icons, STAGES):
            self._nav_btn(icon, stage)

        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=18, pady=10)

        # status badge
        self.status_var = tk.StringVar(value="No dataset loaded")
        tk.Label(self, textvariable=self.status_var, bg=PANEL, fg=MUTED,
                 font=(SANS, 8), wraplength=160, justify="left",
                 pady=0).pack(fill="x", padx=18)

    def _nav_btn(self, icon, label_text):
        f = tk.Frame(self, bg=PANEL, cursor="hand2")
        f.pack(fill="x", pady=1)
        inner = tk.Frame(f, bg=PANEL, padx=18, pady=8)
        inner.pack(fill="x")
        tk.Label(inner, text=f"{icon}  {label_text}", bg=PANEL, fg=MUTED,
                 font=(SANS, 10), anchor="w").pack(fill="x")
        f.bind("<Button-1>",  lambda e, s=label_text: self._click(s))
        inner.bind("<Button-1>", lambda e, s=label_text: self._click(s))
        for w in inner.winfo_children():
            w.bind("<Button-1>", lambda e, s=label_text: self._click(s))
        self.btn_map[label_text] = (f, inner)

    def _click(self, stage):
        self.set_active(stage)
        self.on_select(stage)

    def set_active(self, stage):
        if self.active:
            f, inner = self.btn_map[self.active]
            f.config(bg=PANEL); inner.config(bg=PANEL)
            for w in inner.winfo_children():
                w.config(bg=PANEL, fg=MUTED)
        self.active = stage
        f, inner = self.btn_map[stage]
        f.config(bg=BG); inner.config(bg=BG)
        for w in inner.winfo_children():
            w.config(bg=BG, fg=TEXT)


# ══════════════════════════════════════════════════════════════════════════════
# STATUS BAR
# ══════════════════════════════════════════════════════════════════════════════
class StatusBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BORDER, height=28)
        self.pack_propagate(False)
        self._var = tk.StringVar(value="Ready")
        tk.Label(self, textvariable=self._var, bg=BORDER, fg=MUTED,
                 font=(SANS, 9), padx=14).pack(side="left")
        self._prog = ttk.Progressbar(self, length=140, mode="indeterminate")
        self._prog.pack(side="right", padx=14, pady=4)

    def set(self, msg): self._var.set(msg)
    def start(self): self._prog.start(12)
    def stop(self):  self._prog.stop()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE BASE
# ══════════════════════════════════════════════════════════════════════════════
class BasePage(tk.Frame):
    def __init__(self, master, ctx, status_bar):
        super().__init__(master, bg=BG)
        self.ctx = ctx
        self.sb  = status_bar

    def header(self, title, subtitle=""):
        f = tk.Frame(self, bg=BG, pady=24, padx=32)
        f.pack(fill="x")
        label(f, title, size=18, weight="bold", bg=BG).pack(anchor="w")
        if subtitle:
            label(f, subtitle, size=10, color=MUTED, bg=BG).pack(anchor="w", pady=(2,0))
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=32)

    def card(self, parent, title="", pady=14, padx=18):
        outer = tk.Frame(parent, bg=PANEL, pady=pady, padx=padx,
                         highlightbackground=BORDER, highlightthickness=1)
        if title:
            label(outer, title, size=9, weight="bold", color=MUTED).pack(anchor="w", pady=(0,8))
        return outer

    def run_thread(self, fn, done_cb=None):
        self.sb.start()
        def _run():
            try:    fn()
            finally:
                self.sb.stop()
                if done_cb: self.after(0, done_cb)
        threading.Thread(target=_run, daemon=True).start()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — IMPORT
# ══════════════════════════════════════════════════════════════════════════════
class ImportPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Import Dataset",
                    "Load a CSV, Excel, JSON, XML, ZIP or image folder")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        # drop zone
        self.drop = tk.Frame(body, bg=PANEL, height=160,
                             highlightbackground=ACCENT,
                             highlightthickness=2)
        self.drop.pack(fill="x", pady=(0, 20))
        self.drop.pack_propagate(False)
        label(self.drop, "Drop a file here  —  or browse below",
              size=12, color=MUTED).place(relx=.5, rely=.5, anchor="center")

        # path row
        row = tk.Frame(body, bg=BG)
        row.pack(fill="x")
        self.path_var = tk.StringVar()
        e = tk.Entry(row, textvariable=self.path_var, bg=PANEL, fg=TEXT,
                     insertbackground=TEXT, font=(MONO, 10), relief="flat",
                     highlightbackground=BORDER, highlightthickness=1)
        e.pack(side="left", fill="x", expand=True, ipady=8, padx=(0,10))
        button(row, "Browse…", self._browse).pack(side="left")
        button(row, "Load", self._load, accent=True).pack(side="left", padx=(8,0))

        # info card
        self.info_card = self.card(body, "Dataset Info")
        self.info_card.pack(fill="x", pady=(20,0))
        self.info_lbl = label(self.info_card, "No dataset loaded yet.",
                              color=MUTED, size=9)
        self.info_lbl.pack(anchor="w")

    def _browse(self):
        from tkinter import filedialog
        p = filedialog.askopenfilename(
            filetypes=[("Supported files",
                        "*.csv *.xlsx *.xls *.json *.xml *.zip"),
                       ("All files","*.*")])
        if p:
            self.path_var.set(p)

    def _load(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showwarning("No file", "Please select a file first.")
            return
        self.sb.set(f"Loading {path} …")
        def _do():
            import sys, os
            sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from import_.import_manager import ImportManager
            df = ImportManager().load(path)
            self.ctx.raw_data    = df
            self.ctx.source_files = [path]
            rows, cols = df.shape
            self.after(0, lambda: self.info_lbl.config(
                fg=SUCCESS,
                text=f"✓  Loaded  {rows:,} rows × {cols} columns   |  {path}"))
            self.sb.set(f"Loaded {rows:,} rows × {cols} cols")
        self.run_thread(_do)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — SCHEMA
# ══════════════════════════════════════════════════════════════════════════════
class SchemaPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Schema Inspector", "Detected column types and nullability")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        btn_row = tk.Frame(body, bg=BG)
        btn_row.pack(fill="x", pady=(0,14))
        button(btn_row, "Detect Schema", self._detect).pack(side="left")

        # table
        cols = ("Column","Type","Non-null","Unique","Sample")
        self.tree = ttk.Treeview(body, columns=cols, show="headings", height=22)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=PANEL, foreground=TEXT,
                        fieldbackground=PANEL, rowheight=26,
                        font=(SANS, 9))
        style.configure("Treeview.Heading",
                        background=BG, foreground=MUTED,
                        font=(SANS, 9, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT)])
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=130, anchor="w")
        sb2 = tk.Scrollbar(body, command=self.tree.yview, bg=BORDER)
        self.tree.configure(yscrollcommand=sb2.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb2.pack(side="left", fill="y")

    def _detect(self):
        if self.ctx.raw_data is None:
            messagebox.showwarning("No data", "Import a dataset first.")
            return
        self.sb.set("Detecting schema…")
        def _do():
            import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from analysis.schema_detector import SchemaDetector
            df = self.ctx.raw_data
            self.ctx.schema = SchemaDetector().detect(df)
            self.after(0, self._populate)
        self.run_thread(_do)

    def _populate(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        df = self.ctx.raw_data
        for col, typ in self.ctx.schema.items():
            nonnull = int(df[col].notna().sum())
            unique  = int(df[col].nunique())
            sample  = str(df[col].dropna().iloc[0]) if nonnull else "—"
            self.tree.insert("", "end", values=(col, typ, nonnull, unique, sample[:40]))
        self.sb.set("Schema detected.")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — EDA
# ══════════════════════════════════════════════════════════════════════════════
class EDAPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Exploratory Data Analysis", "Profile, statistics and distribution")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        button(body, "Run EDA", self._run).pack(anchor="w", pady=(0,14))

        self.txt_frame, self.txt = scrolled_text(body, height=26)
        self.txt_frame.pack(fill="both", expand=True)

    def _run(self):
        if self.ctx.raw_data is None:
            messagebox.showwarning("No data","Import a dataset first.")
            return
        self.sb.set("Running EDA…")
        def _do():
            import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from analysis.profile_engine     import ProfileEngine
            from analysis.statistical_engine import StatisticalEngine
            from analysis.distribution_engine import DistributionEngine
            from analysis.imbalance_engine   import ImbalanceEngine
            import json
            df = self.ctx.raw_data
            profile = ProfileEngine().profile(df)
            stats   = StatisticalEngine().compute(df)
            dist    = DistributionEngine().classify(df)
            report  = {"profile": profile, "statistics": stats, "distributions": dist}
            self.ctx.eda_report = report
            txt = json.dumps(report, indent=2, default=str)
            self.after(0, lambda: self._show(txt))
        self.run_thread(_do, lambda: self.sb.set("EDA complete."))

    def _show(self, txt):
        self.txt.config(state="normal")
        self.txt.delete("1.0","end")
        self.txt.insert("end", txt)
        self.txt.config(state="disabled")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — CLEAN
# ══════════════════════════════════════════════════════════════════════════════
class CleaningPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Data Cleaning", "Remove duplicates, fill nulls, drop constants")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        # options card
        opt = self.card(body, "Options")
        opt.pack(fill="x", pady=(0,16))

        grid = tk.Frame(opt, bg=PANEL)
        grid.pack(fill="x")

        tk.Label(grid, text="Missing value strategy:", bg=PANEL, fg=TEXT,
                 font=(SANS,10)).grid(row=0, column=0, sticky="w", pady=4)
        self.fill_var = tk.StringVar(value="mean")
        for i, v in enumerate(["mean","drop","zero"]):
            tk.Radiobutton(grid, text=v, variable=self.fill_var, value=v,
                           bg=PANEL, fg=TEXT, selectcolor=BG,
                           activebackground=PANEL,
                           font=(SANS,10)).grid(row=0, column=i+1, padx=10)

        button(body, "Run Cleaning", self._clean).pack(anchor="w", pady=(0,16))

        self.result_lbl = label(body, "", color=MUTED, bg=BG, size=10)
        self.result_lbl.pack(anchor="w")

    def _clean(self):
        if self.ctx.raw_data is None:
            messagebox.showwarning("No data","Import a dataset first.")
            return
        self.sb.set("Cleaning…")
        strategy = {"fill_missing": self.fill_var.get()}
        def _do():
            import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from preprocessing.cleaning_pipeline import CleaningPipeline
            clean = CleaningPipeline().run(self.ctx.raw_data, strategy)
            self.ctx.cleaned_data = clean
            r0, c0 = self.ctx.raw_data.shape
            r1, c1 = clean.shape
            msg = (f"✓  {r0:,}→{r1:,} rows  |  {c0}→{c1} cols  "
                   f"|  strategy: {strategy['fill_missing']}")
            self.after(0, lambda: self.result_lbl.config(text=msg, fg=SUCCESS))
        self.run_thread(_do, lambda: self.sb.set("Cleaning done."))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — FEATURES
# ══════════════════════════════════════════════════════════════════════════════
class FeaturesPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Feature Engineering", "Encode categoricals, scale numerics")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        opt = self.card(body, "Options")
        opt.pack(fill="x", pady=(0,16))

        grid = tk.Frame(opt, bg=PANEL)
        grid.pack(fill="x")

        tk.Label(grid, text="Encoding:", bg=PANEL, fg=TEXT,
                 font=(SANS,10)).grid(row=0,column=0,sticky="w",pady=4)
        self.enc_var = tk.StringVar(value="onehot")
        for i,v in enumerate(["onehot","label"]):
            tk.Radiobutton(grid, text=v, variable=self.enc_var, value=v,
                           bg=PANEL, fg=TEXT, selectcolor=BG,
                           activebackground=PANEL,
                           font=(SANS,10)).grid(row=0,column=i+1,padx=10)

        tk.Label(grid, text="Scaling:", bg=PANEL, fg=TEXT,
                 font=(SANS,10)).grid(row=1,column=0,sticky="w",pady=4)
        self.scl_var = tk.StringVar(value="standard")
        for i,v in enumerate(["standard","minmax","robust"]):
            tk.Radiobutton(grid, text=v, variable=self.scl_var, value=v,
                           bg=PANEL, fg=TEXT, selectcolor=BG,
                           activebackground=PANEL,
                           font=(SANS,10)).grid(row=1,column=i+1,padx=10)

        button(body, "Apply Features", self._apply).pack(anchor="w", pady=(0,16))
        self.result_lbl = label(body,"",color=MUTED,bg=BG,size=10)
        self.result_lbl.pack(anchor="w")

    def _apply(self):
        src = self.ctx.cleaned_data or self.ctx.raw_data
        if src is None:
            messagebox.showwarning("No data","Import / clean data first.")
            return
        enc = self.enc_var.get()
        scl = self.scl_var.get()
        self.sb.set("Engineering features…")
        def _do():
            import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from features.encoding_engine import EncodingEngine
            from features.scaling_engine  import ScalingEngine
            df = EncodingEngine().encode(src, enc)
            df = ScalingEngine().scale(df, scl)
            self.ctx.feature_config = {"encoding": enc, "scaling": scl}
            # store back as cleaned_data for downstream steps
            self.ctx.cleaned_data = df
            msg = f"✓  {df.shape[1]} features  |  enc={enc}  scl={scl}"
            self.after(0, lambda: self.result_lbl.config(text=msg, fg=SUCCESS))
        self.run_thread(_do, lambda: self.sb.set("Features ready."))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — MODELS
# ══════════════════════════════════════════════════════════════════════════════
class ModelsPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Model Selection", "Choose target, detect task, pick a model")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        opt = self.card(body, "Configuration")
        opt.pack(fill="x", pady=(0,16))

        grid = tk.Frame(opt, bg=PANEL)
        grid.pack(fill="x")

        tk.Label(grid, text="Target column:", bg=PANEL, fg=TEXT,
                 font=(SANS,10)).grid(row=0,column=0,sticky="w",pady=6)
        self.target_var = tk.StringVar()
        self.target_entry = tk.Entry(grid, textvariable=self.target_var,
                                     bg=BG, fg=TEXT, insertbackground=TEXT,
                                     font=(MONO,10), relief="flat",
                                     highlightbackground=BORDER,
                                     highlightthickness=1, width=24)
        self.target_entry.grid(row=0,column=1,padx=10,ipady=6)

        tk.Label(grid, text="Dataset size:", bg=PANEL, fg=TEXT,
                 font=(SANS,10)).grid(row=1,column=0,sticky="w",pady=6)
        self.size_var = tk.StringVar(value="small")
        for i,v in enumerate(["small","large"]):
            tk.Radiobutton(grid, text=v, variable=self.size_var, value=v,
                           bg=PANEL, fg=TEXT, selectcolor=BG,
                           activebackground=PANEL,
                           font=(SANS,10)).grid(row=1,column=i+1,padx=10)

        button(body, "Detect Task & Recommend Models", self._detect).pack(anchor="w")

        res = self.card(body, "Recommendations")
        res.pack(fill="x", pady=(16,0))
        self.rec_lbl = label(res,"Run detection first.",color=MUTED)
        self.rec_lbl.pack(anchor="w")

        # model picker
        self.model_var = tk.StringVar(value="RandomForest")
        tk.Label(body, text="Selected model:", bg=BG, fg=MUTED,
                 font=(SANS,9)).pack(anchor="w",pady=(14,4))
        self.model_combo = ttk.Combobox(body, textvariable=self.model_var,
                                         values=["RandomForest","XGBoost","LightGBM"],
                                         state="readonly", width=24)
        self.model_combo.pack(anchor="w")

    def _detect(self):
        src = self.ctx.cleaned_data or self.ctx.raw_data
        if src is None:
            messagebox.showwarning("No data","Import data first.")
            return
        target = self.target_var.get().strip()
        if not target:
            messagebox.showwarning("No target","Enter a target column name.")
            return
        def _do():
            import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from models.task_detector         import TaskDetector
            from models.recommendation_engine import ModelRecommender
            task  = TaskDetector().detect(src, target)
            recs  = ModelRecommender().recommend(task, self.size_var.get())
            self.ctx.target_column = target
            self.ctx.task_type     = task
            self.ctx.model_config  = {"model": self.model_var.get()}
            msg = f"Task: {task.upper()}    |    Recommended: {', '.join(recs)}"
            self.after(0, lambda: (
                self.rec_lbl.config(text=msg, fg=SUCCESS),
                self.model_combo.config(values=recs),
                self.model_var.set(recs[0])
            ))
        self.run_thread(_do, lambda: self.sb.set("Task detected."))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — TRAIN
# ══════════════════════════════════════════════════════════════════════════════
class TrainPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Train Model", "Fit and evaluate the selected model")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        self.go_btn = button(body, "▶  Start Training", self._train)
        self.go_btn.pack(anchor="w", pady=(0,16))

        self.log_frame, self.log = scrolled_text(body, height=22)
        self.log_frame.pack(fill="both", expand=True)

    def _log(self, msg):
        self.log.config(state="normal")
        self.log.insert("end", msg+"\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def _train(self):
        src = self.ctx.cleaned_data or self.ctx.raw_data
        if src is None or not self.ctx.target_column:
            messagebox.showwarning("Missing","Complete Import → Models steps first.")
            return
        self.sb.set("Training…")
        target = self.ctx.target_column
        task   = self.ctx.task_type or "classification"
        model_name = (self.ctx.model_config or {}).get("model","RandomForest")
        self.after(0,lambda: self._log(f"Target    : {target}"))
        self.after(0,lambda: self._log(f"Task      : {task}"))
        self.after(0,lambda: self._log(f"Model     : {model_name}"))
        self.after(0,lambda: self._log("Training…"))
        def _do():
            import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from training.training_engine   import TrainingEngine
            from training.evaluation_engine import EvaluationEngine
            try:
                # keep only numeric for training
                df_num = src.select_dtypes(include="number").dropna()
                if target not in df_num.columns:
                    raise ValueError(f"Target '{target}' not numeric after encoding.")
                model, metrics = TrainingEngine().train(df_num, target, task, model_name)
                self.ctx.training_results = {"metrics": metrics, "model": model}
                self.after(0, lambda: self._log(f"\n✓ Metrics: {metrics}"))
                self.sb.set("Training complete.")
            except Exception as ex:
                self.after(0, lambda: self._log(f"\n✗ Error: {ex}"))
                self.sb.set("Training failed.")
        self.run_thread(_do)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — RESULTS
# ══════════════════════════════════════════════════════════════════════════════
class ResultsPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Training Results", "Metrics from the last training run")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        button(body,"Refresh Results", self._refresh).pack(anchor="w",pady=(0,16))

        self.cards_frame = tk.Frame(body, bg=BG)
        self.cards_frame.pack(fill="both", expand=True)

    def _refresh(self):
        for w in self.cards_frame.winfo_children():
            w.destroy()
        res = self.ctx.training_results
        if not res:
            label(self.cards_frame,"No results yet — run training first.",
                  color=MUTED, bg=BG).pack(anchor="w")
            return
        metrics = res.get("metrics", {})
        row = tk.Frame(self.cards_frame, bg=BG)
        row.pack(fill="x")
        for k,v in metrics.items():
            card = tk.Frame(row, bg=PANEL, padx=22, pady=18,
                            highlightbackground=BORDER, highlightthickness=1)
            card.pack(side="left", padx=(0,12))
            label(card, f"{v:.4f}", size=22, weight="bold", color=ACCENT).pack()
            label(card, k.upper(), size=8, color=MUTED).pack()
        label(self.cards_frame,
              f"\nModel : {self.ctx.model_config}\n"
              f"Task  : {self.ctx.task_type}",
              color=MUTED, size=9, bg=BG).pack(anchor="w", pady=(14,0))


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — EXPORT
# ══════════════════════════════════════════════════════════════════════════════
class ExportPage(BasePage):
    def __init__(self, master, ctx, sb):
        super().__init__(master, ctx, sb)
        self.header("Export Deployment Package",
                    "Save model + schema + config + requirements")

        body = tk.Frame(self, bg=BG, padx=32, pady=20)
        body.pack(fill="both", expand=True)

        opt = self.card(body,"Output directory")
        opt.pack(fill="x", pady=(0,16))
        self.out_var = tk.StringVar(value="output/")
        row = tk.Frame(opt, bg=PANEL)
        row.pack(fill="x")
        tk.Entry(row, textvariable=self.out_var, bg=BG, fg=TEXT,
                 insertbackground=TEXT, font=(MONO,10), relief="flat",
                 highlightbackground=BORDER, highlightthickness=1
                 ).pack(side="left", fill="x", expand=True, ipady=7, padx=(0,10))
        button(row, "Choose…", self._choose_dir, accent=False).pack(side="left")

        button(body, "⬇  Export Package", self._export).pack(anchor="w",pady=(0,16))

        self.res_lbl = label(body,"",color=MUTED,bg=BG,size=10)
        self.res_lbl.pack(anchor="w")

    def _choose_dir(self):
        from tkinter import filedialog
        d = filedialog.askdirectory()
        if d: self.out_var.set(d)

    def _export(self):
        res = self.ctx.training_results
        if not res or "model" not in res:
            messagebox.showwarning("No model","Train a model first.")
            return
        out = self.out_var.get().strip()
        self.sb.set("Exporting…")
        def _do():
            import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
            from deployment.exporters import DeploymentExporter
            DeploymentExporter().export(
                res["model"],
                self.ctx.schema or {},
                {"task": self.ctx.task_type,
                 "target": self.ctx.target_column,
                 "model": self.ctx.model_config},
                out)
            files = os.listdir(out)
            msg = f"✓  Exported to {out}/  →  {', '.join(files)}"
            self.after(0, lambda: self.res_lbl.config(text=msg, fg=SUCCESS))
        self.run_thread(_do, lambda: self.sb.set("Export complete."))


# ══════════════════════════════════════════════════════════════════════════════
# ROOT APP
# ══════════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ML Pipeline")
        self.geometry("1100x720")
        self.minsize(900, 600)
        self.configure(bg=BG)

        # shared context
        import sys, os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from context.dataset_context import DatasetContext
        self.ctx = DatasetContext()

        # layout
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x")

        self.sidebar = Sidebar(self, self._show_page)
        self.sidebar.pack(side="left", fill="y")

        tk.Frame(self, bg=BORDER, width=1).pack(side="left", fill="y")

        self.content = tk.Frame(self, bg=BG)
        self.content.pack(side="left", fill="both", expand=True)

        # build pages
        self.pages = {
            "Import":   ImportPage(self.content, self.ctx, self.status_bar),
            "Schema":   SchemaPage(self.content, self.ctx, self.status_bar),
            "EDA":      EDAPage(self.content, self.ctx, self.status_bar),
            "Clean":    CleaningPage(self.content, self.ctx, self.status_bar),
            "Features": FeaturesPage(self.content, self.ctx, self.status_bar),
            "Models":   ModelsPage(self.content, self.ctx, self.status_bar),
            "Train":    TrainPage(self.content, self.ctx, self.status_bar),
            "Results":  ResultsPage(self.content, self.ctx, self.status_bar),
            "Export":   ExportPage(self.content, self.ctx, self.status_bar),
        }
        for p in self.pages.values():
            p.place(relx=0, rely=0, relwidth=1, relheight=1)

        self._show_page("Import")

    def _show_page(self, name):
        self.pages[name].lift()
        self.sidebar.set_active(name)
        self.status_bar.set(f"{name} page")


def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
