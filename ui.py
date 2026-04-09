import tkinter as tk
from tkinter import messagebox, ttk

from demo_fixture import DEMO_STEPS, DemoStep
from songs_lru_cache import SongsLRUCache


class SongsCacheApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Songs LRU Cache")
        self.root.geometry("1120x760")
        self.root.minsize(980, 680)

        self.capacity_var = tk.IntVar(value=5)
        self.song_name_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready.")
        self.demo_progress_var = tk.StringVar(value="Demo idle")
        self.demo_job: str | None = None
        self.demo_index = 0

        self.cache = SongsLRUCache(capacity=self.capacity_var.get())

        self._configure_styles()
        self._build_interface()
        self._bind_shortcuts()
        self._seed_demo_data()
        self.refresh_view()

    def _configure_styles(self) -> None:
        self.root.configure(bg="#f4f7fb")
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("App.TFrame", background="#f4f7fb")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure(
            "CardTitle.TLabel",
            background="#ffffff",
            foreground="#20304a",
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "CardValue.TLabel",
            background="#ffffff",
            foreground="#0b5ed7",
            font=("Segoe UI", 15, "bold"),
        )
        style.configure(
            "HeaderTitle.TLabel",
            background="#f4f7fb",
            foreground="#152238",
            font=("Segoe UI", 20, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background="#f4f7fb",
            foreground="#607086",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Badge.TLabel",
            background="#dbeafe",
            foreground="#1d4ed8",
            font=("Segoe UI", 10, "bold"),
            padding=(10, 5),
        )
        style.configure("Primary.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TLabelframe", background="#f4f7fb")
        style.configure(
            "TLabelframe.Label",
            foreground="#20304a",
            font=("Segoe UI", 10, "bold"),
        )

    def _bind_shortcuts(self) -> None:
        self.root.bind("<Control-r>", lambda _event: self.run_demo())
        self.root.bind("<Escape>", lambda _event: self.stop_demo())
        self.root.bind("<Control-l>", lambda _event: self.clear_cache())

    def _build_interface(self) -> None:
        main_frame = ttk.Frame(self.root, padding=18, style="App.TFrame")
        main_frame.pack(fill="both", expand=True)

        header_frame = ttk.Frame(main_frame, style="App.TFrame")
        header_frame.pack(fill="x", pady=(0, 16))

        header_text_frame = ttk.Frame(header_frame, style="App.TFrame")
        header_text_frame.pack(side="left", fill="x", expand=True)

        header_label = ttk.Label(
            header_text_frame,
            text="Songs LRU Cache Visualizer",
            style="HeaderTitle.TLabel",
        )
        header_label.pack(anchor="w")

        description_label = ttk.Label(
            header_text_frame,
            text=(
                "Explore how the cache updates recency, removes the oldest song "
                "and keeps the doubly linked list in sync."
            ),
            style="Muted.TLabel",
        )
        description_label.pack(anchor="w", pady=(4, 0))

        badge_label = ttk.Label(
            header_frame,
            text="Shortcuts: Ctrl+R demo | Esc stop | Ctrl+L clear",
            style="Badge.TLabel",
        )
        badge_label.pack(side="right", anchor="n")

        controls_frame = ttk.LabelFrame(main_frame, text="Controls", padding=14)
        controls_frame.pack(fill="x")

        ttk.Label(controls_frame, text="Song name:").grid(row=0, column=0, sticky="w")
        self.song_combobox = ttk.Combobox(
            controls_frame,
            textvariable=self.song_name_var,
            width=34,
            state="normal",
        )
        self.song_combobox.grid(row=0, column=1, padx=(8, 16), sticky="ew")
        self.song_combobox.bind("<Return>", lambda _event: self.add_song())

        ttk.Label(controls_frame, text="Capacity:").grid(row=0, column=2, sticky="w")
        capacity_spinbox = ttk.Spinbox(
            controls_frame,
            from_=1,
            to=100,
            textvariable=self.capacity_var,
            width=6,
        )
        capacity_spinbox.grid(row=0, column=3, padx=(8, 16), sticky="w")

        apply_capacity_button = ttk.Button(
            controls_frame,
            text="Create new cache",
            command=self.reset_cache,
        )
        apply_capacity_button.grid(row=0, column=4, sticky="w")

        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.grid(row=1, column=0, columnspan=5, pady=(14, 0), sticky="w")

        self.add_button = ttk.Button(
            buttons_frame,
            text="Add song",
            command=self.add_song,
            style="Primary.TButton",
        )
        self.add_button.pack(side="left", padx=(0, 8))
        self.use_button = ttk.Button(buttons_frame, text="Use song", command=self.use_song)
        self.use_button.pack(side="left", padx=(0, 8))
        self.remove_button = ttk.Button(
            buttons_frame,
            text="Remove song",
            command=self.remove_song,
        )
        self.remove_button.pack(side="left", padx=(0, 8))
        self.remove_recent_button = ttk.Button(
            buttons_frame,
            text="Remove most recent",
            command=self.remove_most_recent,
        )
        self.remove_recent_button.pack(side="left", padx=(0, 8))
        self.remove_oldest_button = ttk.Button(
            buttons_frame,
            text="Remove oldest",
            command=self.remove_oldest,
        )
        self.remove_oldest_button.pack(side="left", padx=(0, 8))
        self.clear_button = ttk.Button(buttons_frame, text="Clear cache", command=self.clear_cache)
        self.clear_button.pack(side="left")
        self.run_demo_button = ttk.Button(
            buttons_frame,
            text="Run demo",
            command=self.run_demo,
        )
        self.run_demo_button.pack(side="left", padx=(8, 0))
        self.stop_demo_button = ttk.Button(
            buttons_frame,
            text="Stop demo",
            command=self.stop_demo,
        )
        self.stop_demo_button.pack(side="left", padx=(8, 0))

        controls_frame.columnconfigure(1, weight=1)

        stats_grid = ttk.Frame(main_frame, style="App.TFrame")
        stats_grid.pack(fill="x", pady=(16, 16))
        stats_grid.columnconfigure((0, 1, 2, 3), weight=1)

        size_card = ttk.Frame(stats_grid, padding=14, style="Card.TFrame")
        size_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        ttk.Label(size_card, text="Cache size", style="CardTitle.TLabel").pack(anchor="w")
        self.size_label = ttk.Label(size_card, text="0 / 0", style="CardValue.TLabel")
        self.size_label.pack(anchor="w", pady=(8, 0))

        recent_card = ttk.Frame(stats_grid, padding=14, style="Card.TFrame")
        recent_card.grid(row=0, column=1, sticky="nsew", padx=8)
        ttk.Label(recent_card, text="Most recent", style="CardTitle.TLabel").pack(anchor="w")
        self.most_recent_label = ttk.Label(recent_card, text="None", style="CardValue.TLabel")
        self.most_recent_label.pack(anchor="w", pady=(8, 0))

        oldest_card = ttk.Frame(stats_grid, padding=14, style="Card.TFrame")
        oldest_card.grid(row=0, column=2, sticky="nsew", padx=8)
        ttk.Label(oldest_card, text="Oldest", style="CardTitle.TLabel").pack(anchor="w")
        self.oldest_label = ttk.Label(oldest_card, text="None", style="CardValue.TLabel")
        self.oldest_label.pack(anchor="w", pady=(8, 0))

        demo_card = ttk.Frame(stats_grid, padding=14, style="Card.TFrame")
        demo_card.grid(row=0, column=3, sticky="nsew", padx=(8, 0))
        ttk.Label(demo_card, text="Demo status", style="CardTitle.TLabel").pack(anchor="w")
        self.demo_label = ttk.Label(
            demo_card,
            textvariable=self.demo_progress_var,
            style="CardValue.TLabel",
        )
        self.demo_label.pack(anchor="w", pady=(8, 0))

        visualization_frame = ttk.LabelFrame(main_frame, text="Linked list view", padding=12)
        visualization_frame.pack(fill="x", pady=(0, 16))

        self.visual_canvas = tk.Canvas(
            visualization_frame,
            height=150,
            bg="#ffffff",
            bd=0,
            highlightthickness=0,
        )
        self.visual_canvas.pack(fill="x", expand=True)

        lists_frame = ttk.Panedwindow(main_frame, orient="horizontal")
        lists_frame.pack(fill="both", expand=True)

        recent_frame = ttk.LabelFrame(
            lists_frame,
            text="Recent -> Oldest",
            padding=12,
        )
        lists_frame.add(recent_frame, weight=1)

        recent_list_frame = ttk.Frame(recent_frame)
        recent_list_frame.pack(fill="both", expand=True)
        self.recent_listbox = tk.Listbox(
            recent_list_frame,
            height=16,
            activestyle="none",
            font=("Segoe UI", 10),
            selectbackground="#dbeafe",
            selectforeground="#0f172a",
            bg="#ffffff",
            relief="flat",
        )
        recent_scrollbar = ttk.Scrollbar(
            recent_list_frame,
            orient="vertical",
            command=self.recent_listbox.yview,
        )
        self.recent_listbox.configure(yscrollcommand=recent_scrollbar.set)
        self.recent_listbox.pack(side="left", fill="both", expand=True)
        recent_scrollbar.pack(side="right", fill="y")
        self.recent_listbox.bind("<<ListboxSelect>>", self._sync_song_entry_from_list)

        reverse_frame = ttk.LabelFrame(
            lists_frame,
            text="Oldest -> Recent",
            padding=12,
        )
        lists_frame.add(reverse_frame, weight=1)

        reverse_list_frame = ttk.Frame(reverse_frame)
        reverse_list_frame.pack(fill="both", expand=True)
        self.reverse_listbox = tk.Listbox(
            reverse_list_frame,
            height=16,
            activestyle="none",
            font=("Segoe UI", 10),
            selectbackground="#dbeafe",
            selectforeground="#0f172a",
            bg="#ffffff",
            relief="flat",
        )
        reverse_scrollbar = ttk.Scrollbar(
            reverse_list_frame,
            orient="vertical",
            command=self.reverse_listbox.yview,
        )
        self.reverse_listbox.configure(yscrollcommand=reverse_scrollbar.set)
        self.reverse_listbox.pack(side="left", fill="both", expand=True)
        reverse_scrollbar.pack(side="right", fill="y")
        self.reverse_listbox.bind("<<ListboxSelect>>", self._sync_song_entry_from_list)

        log_frame = ttk.LabelFrame(main_frame, text="Operation log", padding=12)
        log_frame.pack(fill="both", expand=True, pady=(16, 0))

        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.pack(fill="both", expand=True)
        self.log_text = tk.Text(
            log_text_frame,
            height=8,
            wrap="word",
            state="disabled",
            font=("Consolas", 10),
            bg="#ffffff",
            relief="flat",
        )
        log_scrollbar = ttk.Scrollbar(
            log_text_frame,
            orient="vertical",
            command=self.log_text.yview,
        )
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")

        status_frame = ttk.Frame(main_frame, style="App.TFrame")
        status_frame.pack(fill="x", pady=(12, 0))
        ttk.Label(status_frame, text="Status:", style="CardTitle.TLabel").pack(side="left")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style="Muted.TLabel")
        status_label.pack(side="left", padx=(8, 0))

    def _seed_demo_data(self) -> None:
        for name in [
            "Imagine",
            "Bohemian Rhapsody",
            "Hotel California",
            "Hey Jude",
            "Billie Jean",
        ]:
            self.cache.add_song(name)
        self._log("Loaded demo songs.")
        self._refresh_song_suggestions()

    def _notify_eviction(self, removed_name: str) -> None:
        self._log(f'LRU rule removed the oldest song: "{removed_name}".')
        messagebox.showinfo(
            "Song removed from cache",
            f'The cache reached its limit, so "{removed_name}" was removed.',
        )

    def _selected_song_name(self) -> str:
        return self.song_name_var.get().strip()

    def _refresh_song_suggestions(self) -> None:
        suggestions = self.cache.list_recent_to_oldest()
        self.song_combobox["values"] = suggestions

    def _update_action_buttons(self) -> None:
        has_songs = len(self.cache) > 0
        demo_running = self.demo_job is not None

        self.use_button.configure(state="normal" if has_songs else "disabled")
        self.remove_button.configure(state="normal" if has_songs else "disabled")
        self.remove_recent_button.configure(state="normal" if has_songs else "disabled")
        self.remove_oldest_button.configure(state="normal" if has_songs else "disabled")
        self.clear_button.configure(state="normal" if has_songs else "disabled")
        self.run_demo_button.configure(state="disabled" if demo_running else "normal")
        self.stop_demo_button.configure(state="normal" if demo_running else "disabled")

    def _sync_song_entry_from_list(self, event: tk.Event) -> None:
        widget = event.widget
        selection = widget.curselection()
        if not selection:
            return

        song_name = widget.get(selection[0])
        self.song_name_var.set(song_name)

    def _log(self, message: str) -> None:
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _draw_cache_visualization(self, recent_songs: list[str]) -> None:
        self.visual_canvas.delete("all")

        canvas_width = max(self.visual_canvas.winfo_width(), 920)
        node_width = 165
        node_height = 56
        gap = 28
        y = 76
        start_x = 20

        if not recent_songs:
            self.visual_canvas.create_text(
                canvas_width / 2,
                y,
                text="Cache is empty. Add songs to see the doubly linked list.",
                fill="#607086",
                font=("Segoe UI", 12),
            )
            return

        for index, song_name in enumerate(recent_songs):
            x1 = start_x + index * (node_width + gap)
            x2 = x1 + node_width
            y1 = y - (node_height / 2)
            y2 = y + (node_height / 2)

            fill_color = "#dbeafe" if index == 0 else "#ffffff"
            outline_color = "#2563eb" if index == 0 else "#bfd1e5"
            label = (
                "Most recent"
                if index == 0
                else "Oldest"
                if index == len(recent_songs) - 1
                else "Node"
            )

            self.visual_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=fill_color,
                outline=outline_color,
                width=2,
            )
            self.visual_canvas.create_text(
                x1 + 12,
                y1 + 14,
                text=label,
                fill="#1d4ed8" if index == 0 else "#607086",
                font=("Segoe UI", 9, "bold"),
                anchor="w",
            )
            self.visual_canvas.create_text(
                x1 + 12,
                y1 + 36,
                text=song_name,
                fill="#152238",
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                width=node_width - 24,
            )

            if index < len(recent_songs) - 1:
                arrow_start = x2
                arrow_end = x2 + gap
                self.visual_canvas.create_line(
                    arrow_start,
                    y,
                    arrow_end,
                    y,
                    fill="#64748b",
                    width=2,
                    arrow="last",
                )
                self.visual_canvas.create_line(
                    arrow_end,
                    y + 14,
                    arrow_start,
                    y + 14,
                    fill="#94a3b8",
                    width=2,
                    arrow="last",
                )
                self.visual_canvas.create_text(
                    x2 + (gap / 2),
                    y - 14,
                    text="next",
                    fill="#64748b",
                    font=("Segoe UI", 8),
                )
                self.visual_canvas.create_text(
                    x2 + (gap / 2),
                    y + 28,
                    text="prev",
                    fill="#94a3b8",
                    font=("Segoe UI", 8),
                )

    def refresh_view(self) -> None:
        recent_songs = self.cache.list_recent_to_oldest()
        reverse_songs = self.cache.list_oldest_to_recent()

        self.recent_listbox.delete(0, "end")
        for song_name in recent_songs:
            self.recent_listbox.insert("end", song_name)

        self.reverse_listbox.delete(0, "end")
        for song_name in reverse_songs:
            self.reverse_listbox.insert("end", song_name)

        most_recent = self.cache.most_recent_song()
        oldest = self.cache.oldest_song()

        self.size_label.configure(text=f"{len(self.cache)} / {self.cache.capacity}")
        self.most_recent_label.configure(text=most_recent.name if most_recent else "None")
        self.oldest_label.configure(text=oldest.name if oldest else "None")
        self._refresh_song_suggestions()
        self._draw_cache_visualization(recent_songs)
        self._update_action_buttons()

    def reset_cache(self) -> None:
        self.stop_demo(update_status=False)
        try:
            capacity = int(self.capacity_var.get())
            self.cache = SongsLRUCache(capacity=capacity)
        except ValueError as error:
            messagebox.showerror("Invalid capacity", str(error))
            return

        self._seed_demo_data()
        self.status_var.set(f"Created a new cache with capacity {self.cache.capacity}.")
        self._log(f"Created a new cache with capacity {self.cache.capacity}.")
        self.refresh_view()

    def add_song(self) -> None:
        song_name = self._selected_song_name()
        if not song_name:
            self.status_var.set("Enter a song name first.")
            return

        previous_size = len(self.cache)
        oldest_before = self.cache.oldest_song()
        self.cache.add_song(song_name)
        oldest_after = self.cache.oldest_song()

        self.status_var.set(f'Added "{song_name}" to the cache.')
        self._log(f'Added "{song_name}" to the cache.')
        self.song_name_var.set("")

        if previous_size == self.cache.capacity and oldest_before != oldest_after:
            removed_name = oldest_before.name if oldest_before else "Unknown"
            self._notify_eviction(removed_name)

        self.refresh_view()

    def use_song(self) -> None:
        song_name = self._selected_song_name()
        if not song_name:
            self.status_var.set("Enter a song name first.")
            return

        song = self.cache.get_song(song_name)
        if song is None:
            self.status_var.set(f'"{song_name}" is not in the cache.')
            self._log(f'Use failed because "{song_name}" was not found.')
            return

        self.status_var.set(f'Used "{song.name}". It is now the most recent song.')
        self._log(f'Used "{song.name}" and moved it to the front.')
        self.refresh_view()

    def remove_song(self) -> None:
        song_name = self._selected_song_name()
        if not song_name:
            self.status_var.set("Enter a song name first.")
            return

        was_removed = self.cache.remove_song(song_name)
        if not was_removed:
            self.status_var.set(f'"{song_name}" is not in the cache.')
            self._log(f'Remove failed because "{song_name}" was not found.')
            return

        self.status_var.set(f'Removed "{song_name}" from the cache.')
        self._log(f'Removed "{song_name}" from the cache.')
        self.song_name_var.set("")
        self.refresh_view()

    def remove_most_recent(self) -> None:
        removed_song = self.cache.remove_most_recent()
        if removed_song is None:
            self.status_var.set("The cache is empty.")
            self._log("Remove most recent failed because the cache is empty.")
            return

        self.status_var.set(f'Removed most recent song: "{removed_song.name}".')
        self._log(f'Removed most recent song: "{removed_song.name}".')
        self.refresh_view()

    def remove_oldest(self) -> None:
        removed_song = self.cache.remove_oldest()
        if removed_song is None:
            self.status_var.set("The cache is empty.")
            self._log("Remove oldest failed because the cache is empty.")
            return

        self.status_var.set(f'Removed oldest song: "{removed_song.name}".')
        self._log(f'Removed oldest song: "{removed_song.name}".')
        self.refresh_view()

    def clear_cache(self) -> None:
        self.stop_demo(update_status=False)
        if len(self.cache) > 0:
            should_clear = messagebox.askyesno(
                "Clear cache",
                "Do you want to remove all songs from the cache?",
            )
            if not should_clear:
                self.status_var.set("Clear operation cancelled.")
                return

        self.cache.clear()
        self.status_var.set("Cleared the cache.")
        self._log("Cleared the cache.")
        self.refresh_view()

    def _execute_demo_step(self, step: DemoStep) -> None:
        self._log(f"Demo step: {step.description}")

        if step.action == "reset":
            self.reset_cache()
            return

        if step.action == "add" and step.song_name is not None:
            self.song_name_var.set(step.song_name)
            self.add_song()
            return

        if step.action == "use" and step.song_name is not None:
            self.song_name_var.set(step.song_name)
            self.use_song()
            return

        if step.action == "remove" and step.song_name is not None:
            self.song_name_var.set(step.song_name)
            self.remove_song()
            return

        if step.action == "remove_oldest":
            self.remove_oldest()
            return

        if step.action == "remove_most_recent":
            self.remove_most_recent()
            return

        self._log(f"Skipped unsupported demo step: {step}")

    def _schedule_next_demo_step(self) -> None:
        if self.demo_index >= len(DEMO_STEPS):
            self.demo_job = None
            self.status_var.set("Demo finished.")
            self.demo_progress_var.set("Demo finished")
            self._log("Demo finished.")
            self._update_action_buttons()
            return

        step = DEMO_STEPS[self.demo_index]
        self.demo_index += 1
        self.demo_progress_var.set(f"Step {self.demo_index} / {len(DEMO_STEPS)}")
        self._execute_demo_step(step)
        self.demo_job = self.root.after(1600, self._schedule_next_demo_step)
        self._update_action_buttons()

    def run_demo(self) -> None:
        if self.demo_job is not None:
            self.status_var.set("The demo is already running.")
            return

        self.demo_index = 0
        self.status_var.set("Running demo scenario.")
        self.demo_progress_var.set(f"Step 0 / {len(DEMO_STEPS)}")
        self._log("Started demo scenario.")
        self._schedule_next_demo_step()

    def stop_demo(self, update_status: bool = True) -> None:
        if self.demo_job is None:
            if update_status:
                self.status_var.set("There is no active demo.")
            return

        self.root.after_cancel(self.demo_job)
        self.demo_job = None
        self.demo_progress_var.set("Demo stopped")
        if update_status:
            self.status_var.set("Demo stopped.")
        self._log("Stopped demo scenario.")
        self._update_action_buttons()


def run_app() -> None:
    root = tk.Tk()
    SongsCacheApp(root)
    root.mainloop()
