# App demos by Bernardo Ferrari

[<img src="showcase/social.jpg" width="720" alt="The six Kotlin apps in the browser showcase">](https://bernaferrari.github.io/)

[Browse the live gallery](https://bernaferrari.github.io/) · [Kotlin Reforge](https://kotlin-reforge.vercel.app/)

These apps run in the browser using Kotlin/Wasm and Compose Multiplatform. Wordkeep and Calcula are usable browser apps. The four Android utilities use sample data so you can explore their screens without device permissions.

## Kotlin apps

### Wordkeep

[<img src="showcase/wordkeep/preview.webp" width="460" alt="Wordkeep notebook on a tablet and Markdown editor on a phone">](https://bernaferrari.github.io/wordkeep/)

Create a note and switch to the Markdown preview.

[Open Wordkeep](https://bernaferrari.github.io/wordkeep/) · [Source code](https://github.com/bernaferrari/wordkeep)

### Calcula

[<img src="showcase/calcula/preview.webp" width="460" alt="Calcula showing a graph, unit conversion, scientific keys, and themes">](https://bernaferrari.github.io/calcula/)

Flick up on 7 for sine, or open the unit converter.

[Open Calcula](https://bernaferrari.github.io/calcula/) · [Source code](https://github.com/bernaferrari/calcula)

### WiFi Weakspot

[<img src="showcase/wifi-weakspot/preview.webp" width="460" alt="WiFi Weakspot channel graphs across 2.4, 5, and 6 GHz">](https://bernaferrari.github.io/wifi-weakspot/)

Choose Allow access to enter the simulation, then open Networks and switch between the 2.4, 5, and 6 GHz channel views. The browser uses sample data.

[Open WiFi Weakspot](https://bernaferrari.github.io/wifi-weakspot/) · [Source code](https://github.com/bernaferrari/wifi-weakspot)

### SDK Monitor

[<img src="showcase/sdkmonitor/preview.webp" width="460" alt="SDK Monitor analytics, app list, and version details">](https://bernaferrari.github.io/sdkmonitor/)

Open an app to see its target SDK and version history. The browser uses sample data.

[Open SDK Monitor](https://bernaferrari.github.io/sdkmonitor/) · [Source code](https://github.com/bernaferrari/SDKMonitor)

### QuietGuard

[<img src="showcase/quietguard/preview.webp" width="460" alt="QuietGuard displaying per-app firewall controls">](https://bernaferrari.github.io/quietguard/)

Toggle Wi-Fi access for a sample app and look through its rules. The browser uses sample data.

[Open QuietGuard](https://bernaferrari.github.io/quietguard/) · [Source code](https://github.com/bernaferrari/QuietGuard)

### Keepout

[<img src="showcase/keepout/preview.webp" width="460" alt="Keepout showing traffic statistics, protection status, and settings">](https://bernaferrari.github.io/keepout/)

Open Activity, then Insights, to see which apps and domains generated sample traffic. The browser uses sample data.

[Open Keepout](https://bernaferrari.github.io/keepout/) · [Source code](https://github.com/bernaferrari/keepout)

## Flutter apps

### Cash Balancer

[<img src="showcase/cash-balancer/preview.webp" width="460" alt="Cash Balancer portfolio showing current and target allocations">](https://bernaferrari.github.io/CashBalancer/)

Enter your balances and target percentages to see how much you would need to move between assets.

[Open Cash Balancer](https://bernaferrari.github.io/CashBalancer/) · [Source code](https://github.com/bernaferrari/CashBalancer)

### More Flutter projects

- [Color Studio](https://bernaferrari.github.io/color-studio/)
- [Color Blindness Simulator](https://bernaferrari.github.io/ColorBlindnessFlutter/)
- [Diagonal Wipe Icon for Flutter](https://bernaferrari.github.io/diagonal-wipe-icon-flutter/)
- [Fast Dark Theme](https://bernaferrari.github.io/fastdarktheme/)
- [HSLuv for Dart](https://bernaferrari.github.io/hsluv-dart/)
- [Random Color Scheme](https://bernaferrari.github.io/RandomColorScheme/)

## More browser demos

- [Diagonal Wipe Icon for Compose](https://bernaferrari.github.io/diagonal-wipe-icon/)
- [Emoji Slider](https://bernaferrari.github.io/EmojiSlider/)
- [Vibe Jam 2025](https://bernaferrari.github.io/vibejam2025/)

## Update a demo

Build the production distribution in the app's source repository with `./gradlew :<module>:wasmJsBrowserDistribution`.

| Demo path | Gradle module |
| --- | --- |
| `wordkeep` | `:webApp` |
| `calcula` | `:webApp` |
| `wifi-weakspot` | `:webDemo` |
| `sdkmonitor` | `:webApp` |
| `quietguard` | `:webApp` |
| `keepout` | `:shared` |

From this repository, import the resulting directory. Pass the source repository's license file when importing a licensed app for the first time.

```sh
python3 scripts/import-demo.py wordkeep /path/to/wordkeep/webApp/build/dist/wasmJs/productionExecutable --license /path/to/wordkeep/LICENSE
python3 -m http.server 8000
```

Open the gallery at `http://localhost:8000/`, launch the updated demo, and check its main interaction before committing. GitHub Pages publishes from the root of `main`. Wordkeep, QuietGuard, and SDK Monitor use a service worker scoped to each demo to enable the browser isolation needed by SQLite.
