import json
import os
import sys
import gettext
import locale
from pathlib import Path
from typing import Optional

from graph import Graph


class I18nManager:
    """
    Class-based internationalization manager using gettext.
    Avoids global install() and provides NullTranslations fallback.
    """

    def __init__(self, domain: str = "messages", locale_dir: Optional[str] = None):
        self.domain = domain
        self.locale_dir = locale_dir or str(Path(__file__).parent / "locale")
        self._current_lang = None
        self._translator = None
        self._setup_encoding()
        self._detect_and_load()

    def _setup_encoding(self):
        """Ensure UTF-8 encoding for terminal output."""
        try:
            if sys.platform == "win32":
                import codecs

                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
                sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
            else:
                locale.setlocale(locale.LC_ALL, "")
        except Exception:
            pass

        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")

    def _detect_and_load(self):
        """Detect system locale and load appropriate translation."""
        loaded_lang = None

        try:
            env_lang = os.environ.get("LANGUAGE") or os.environ.get("LANG", "")
            if env_lang:
                lang_code = env_lang.split("_")[0].split(".")[0]
                self._load_translations(lang_code)
                if isinstance(self._translator, gettext.GNUTranslations):
                    loaded_lang = lang_code
        except Exception:
            pass

        if not loaded_lang:
            try:
                system_lang = locale.getlocale()[0]
                if system_lang:
                    lang_code = system_lang.split("_")[0]
                    self._load_translations(lang_code)
                    if isinstance(self._translator, gettext.GNUTranslations):
                        loaded_lang = lang_code
            except Exception:
                pass

        if loaded_lang:
            self._current_lang = loaded_lang
        else:
            self._translator = gettext.NullTranslations()
            self._current_lang = None

    def _load_translations(self, lang_code: str):
        """Load translations for specified language."""
        try:
            translation = gettext.translation(
                self.domain,
                localedir=self.locale_dir,
                languages=[lang_code],
                class_=gettext.GNUTranslations,
            )
            self._translator = translation
        except FileNotFoundError:
            self._translator = gettext.NullTranslations()

    def set_language(self, lang_code: str) -> bool:
        """Manually set language (e.g., 'en', 'zh'). Returns True on success."""
        try:
            self._load_translations(lang_code)
            self._current_lang = lang_code
            return True
        except Exception:
            return False

    def gettext(self, message: str) -> str:
        """Standard translation (alias for _())."""
        return self._translator.gettext(message)

    def ngettext(self, singular: str, plural: str, count: int) -> str:
        """Plural-aware translation."""
        return self._translator.ngettext(singular, plural, count)

    def pgettext(self, context: str, message: str) -> str:
        """Context-aware translation (disambiguation)."""
        if hasattr(self._translator, "pgettext"):
            return self._translator.pgettext(context, message)
        else:
            return self._translator.gettext(message)

    def get_current_language(self) -> Optional[str]:
        """Return current language code (e.g., 'en', 'zh')."""
        return self._current_lang

    def get_available_languages(self) -> list:
        """Return list of available language codes from locale directory."""
        available = []
        if os.path.exists(self.locale_dir):
            for item in os.listdir(self.locale_dir):
                if os.path.isdir(os.path.join(self.locale_dir, item)):
                    available.append(item)
        return available


class BeijingSubwaySystem:
    def __init__(self):
        self.i18n = I18nManager()
        _ = self.i18n.gettext

        print(_("Initializing Beijing Subway Network Data..."))
        self.stations = set()
        self.edges = []

        self.hell_stations = {"西直门", "东直门", "国贸", "望京西", "平安里"}

        try:
            with open("data/subway_lines.json", "r", encoding="utf-8") as f:
                subway_lines = json.load(f)

            for line_name, line_data in subway_lines.items():
                segments = line_data["segments"]
                for segment in segments:
                    u = segment["from"]
                    v = segment["to"]
                    t = segment["distance_minutes"]
                    self.stations.add(u)
                    self.stations.add(v)
                    self.edges.append((u, v, t))

        except FileNotFoundError as e:
            print(_("Error: Could not find data file - {e}").format(e=e))
            raise
        except json.JSONDecodeError as e:
            print(_("Error: Invalid JSON format in data file - {e}").format(e=e))
            raise
        except Exception as e:
            print(_("Error: Unexpected error loading subway data - {e}").format(e=e))
            raise

        self.sorted_stations = sorted(list(self.stations))
        self.n = len(self.sorted_stations)
        self.name_to_idx = {name: i for i, name in enumerate(self.sorted_stations)}
        self.idx_to_name = {i: name for i, name in enumerate(self.sorted_stations)}

        matrix_data = [[0] * self.n for _ in range(self.n)]
        for u, v, t in self.edges:
            ui, vi = self.name_to_idx[u], self.name_to_idx[v]
            matrix_data[ui][vi] = t
            matrix_data[vi][ui] = t

        self.graph = Graph(matrix_data)
        print(
            _("Initialization Complete! Loaded {n} stations and {edges} track segments.").format(
                n=self.n, edges=self.graph.count_edges() // 2
            )
        )

    def get_station_id(self, name):
        return self.name_to_idx.get(name)

    def print_path(self, path_indices, detail_type="simple"):
        _ = self.i18n.gettext

        if not path_indices:
            print(_("No path found."))
            return

        names = [self.idx_to_name[i] for i in path_indices]
        if detail_type == "simple":
            print(" -> ".join(names))

        detected_hell_stations = [name for name in names if name in self.hell_stations]
        if detected_hell_stations:
            print(
                _(
                    "This route involves stations known for difficult, long, or crowded transfers: {stations}"
                ).format(stations=", ".join(detected_hell_stations))
            )
            print(_("Please prepare for long walks or stairs."))
            print(_("This route may not be best route in real life."))

        return names

    def run_interactive(self):
        _ = self.i18n.gettext
        __ = self.i18n.gettext

        while True:
            print("\n" + "=" * 50)
            print("   " + _("Beijing Subway Graph Navigation System"))
            print("=" * 50)
            print("1. [Dijkstra] " + _("Fastest Route (Time Weighted)"))
            print("2. [BFS] " + _("Least Stops Route"))
            print("3. [DFS] " + _("Random Exploration Path"))
            print("4. [Prim] " + _("Calculate MST Cost (Total Network Length)"))
            print("5. [Degree] " + _("Station Hub Analysis"))
            print("6. [Matrix] " + _("Algebraic Connectivity Path (CPX Experiment)"))
            print("7. [Components] " + _("Check Network Connectivity"))
            print("8. [Simulation] " + _("Simulate Line Disruption (Remove Edge)"))
            print("0. " + _("Exit"))
            print("=" * 50)

            choice = input(_("Enter option number: "))

            if choice == "0":
                break

            elif choice in ["1", "2", "3", "6"]:
                start_name = input(
                    _("Enter start station (e.g., {example}): ").format(example=_("西直门"))
                )
                end_name = input(
                    _("Enter end station (e.g., {example}): ").format(example=_("国贸"))
                )

                s_id = self.get_station_id(start_name)
                e_id = self.get_station_id(end_name)

                if s_id is None or e_id is None:
                    print(_("Error: Station name does not exist. Please check your input."))
                    continue

                if choice == "1":
                    print(
                        _("\nCalculating fastest route from {start} to {end} (Dijkstra)...").format(
                            start=start_name, end=end_name
                        )
                    )
                    path, time = self.graph.find_shortest_path_weight(s_id, e_id)
                    if path:
                        print(_("Estimated Time: {time} minutes").format(time=time))
                        print(_("Route:"))
                        self.print_path(path)
                    else:
                        print(_("Destination unreachable."))

                elif choice == "2":
                    print(
                        _(
                            "\nCalculating route with fewest stops from {start} to {end} (BFS)..."
                        ).format(start=start_name, end=end_name)
                    )
                    path = self.graph.find_shortest_path_bfs(s_id, e_id)
                    if path:
                        print(_("Total Stops: {count} stations").format(count=len(path)))
                        self.print_path(path)

                elif choice == "3":
                    print(_("\nSearching for a feasible path (DFS)..."))
                    path = self.graph.find_path_dfs(s_id, e_id)
                    self.print_path(path)

                elif choice == "6":
                    print(_("\n[Experimental] Computing path via Matrix Multiplication (CPX)..."))
                    res = self.graph.find_shortest_path_cpx(s_id, e_id)
                    print(_("CPX Result: {result}").format(result=res))

            elif choice == "4":
                print(_("\nCalculating Minimum Spanning Tree (Prim's Algorithm)..."))
                mst, cost = self.graph.minimum_spanning_tree_prim(self.graph.data)
                print(
                    _("Minimum weighted length to connect all {n} stations: {cost}").format(
                        n=self.n, cost=cost
                    )
                )

            elif choice == "5":
                name = input(_("Enter station name to query: "))
                sid = self.get_station_id(name)
                if sid is not None:
                    out_d, in_d = self.graph.get_degree(sid)
                    neighbors = self.graph.get_neighbors(sid)
                    n_names = [self.idx_to_name[i] for i in neighbors]
                    print(_("\nAnalysis for {station}:").format(station=name))
                    print(_("- Connectivity Degree: {degree}").format(degree=out_d))
                    print(
                        _("- Neighboring Stations: {stations}").format(stations=", ".join(n_names))
                    )
                    if out_d > 2:
                        print(_("- Verdict: This is a Transfer Hub."))
                    else:
                        print(_("- Verdict: Regular Stop."))

            elif choice == "7":
                print(_("\nAnalyzing network structure..."))
                is_connected = self.graph.is_connected()
                components = self.graph.connected_components()
                print(
                    _("Is network fully connected: {is_connected}").format(
                        is_connected=is_connected
                    )
                )
                print(_("Number of Connected Components: {count}").format(count=len(components)))
                if not is_connected:
                    print(_("Warning: Isolated station groups detected!"))

                print(_("\nChecking Bipartite Property (BFS)..."))
                is_bi = self.graph.is_bipartite_bfs()
                print(_("Is Bipartite Graph: {is_bipartite}").format(is_bipartite=is_bi))

            elif choice == "8":
                print(_("\nSimulating Construction/Failure Mode..."))
                u_name = input(_("Enter disruption start station: "))
                v_name = input(_("Enter disruption end station: "))
                u, v = self.get_station_id(u_name), self.get_station_id(v_name)
                if u is not None and v is not None:
                    print(_("Cutting connection between {u} <-> {v}...").format(u=u_name, v=v_name))
                    self.graph.remove_edge(u, v)
                    self.graph.remove_edge(v, u)
                    print(_("Line segment disrupted. Please replan route to see effects."))

            else:
                print(_("Invalid input."))


if __name__ == "__main__":
    subway_system = BeijingSubwaySystem()
    try:
        subway_system.run_interactive()
    except KeyboardInterrupt:
        print("\nProgram terminated.")
