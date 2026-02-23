*Lumen M5 to M8 is the final `Milestone` Phase Builds*

# Lumen-M5-Ofc-Repo

We has a break from *February 22 to February 28*.
Official M5 Start on *March 1 and launches on late march* as **Source codes**. 
Welcome to this Lumen build **M5** repo.

## Compressing

To compress M5, here are essential tips:
- Compress Top-level dirs (*instead of compressing the whole distro*)

Try these compression types:
- ZIP
- Tar.Gz (TGZ)

**ZIP** and **TGZ** (**.tar.gz**) serve the same high-level goal: bundle many files/directories into one file + reduce size.
But their **internal design** is very different → this creates strong use-case winners depending on what you're distributing / flashing / backing up.

## Workflow

practical workflow tips for developing a custom Linux distribution (especially relevant for something like your Lumen project — targeting ARMv7a, Moto Nexus 6 / shamu compatibility, flashable ZIPs, and very constrained embedded-like Android replacement goals).
These are ordered roughly from beginner-friendly/fast-iteration approaches → deeper from-scratch understanding → production-grade embedded flows.

```
repo init -u https://github.com/your-org/manifest.git -b lumen-15.0 --git-lfs
 repo sync -j8 --force-sync

 # ────────────────────────────────────────────────
 #  Option A: Very clean & safe (recommended today)
 # ────────────────────────────────────────────────

 # 1. Prepare fresh build environment once per week / big sync
 ./lumen/scripts/setup-build-host.sh           # installs packages, sets ccache, etc

 # 2. Everyday workflow (most time-efficient pattern in 2025)
 time (
   repo sync -j6 --no-tags --no-repo-verify    # fast, no history garbage
   source build/envsetup.sh
   lunch lumen_shamu-userdebug

   # Pick only what you actually changed (90% time saving)
   m -j$(nproc --all) \
     bootimage \
     dtboimage \
     vendorbootimage \
     systemimage \
     productimage \
     odmdtboimage    # if device still uses it

   # or even more surgical:
   # m -j$(nproc --all) bootimage systemimage
 )

 # Quick flash only changed partitions (shamu still uses fastboot)
 ./lumen/scripts/fastboot-flash-changed.sh

 # ────────────────────────────────────────────────
 #  Option B: "I want to iterate on one subsystem fast"
 # ────────────────────────────────────────────────

 # Example: Framework / SystemUI / Settings quick iteration
 m -j$(nproc --all) framework-res settings SystemUI
 adb root && adb remount
 adb sync   # or adb push out/target/product/shamu/system/framework/framework-res.apk /system/framework/
 adb shell am crash com.android.systemui   # force restart
 # or
 adb shell stop && adb shell start

 # Example: Kernel / dtb / ramdisk fast cycle
 ./lumen/scripts/build-kernel-only.sh
 ./lumen/scripts/fastboot-flash-kernel-dtbo.sh

 # ────────────────────────────────────────────────
 #  Useful helper scripts worth having in 2025
 # ────────────────────────────────────────────────

 # a) ccache statistics cheat-sheet
 ccache -s
 ccache -M 120G           # set once on big SSD/NVMe

 # b) Compare two builds quickly
 diffoscope out/target/product/shamu/system.img.{old,new}

 # c) Find what pulls in a certain module/library
 m -j1 nothing |& grep -i "libc++fs\|libsqlite\|libcurl"

 # d) Very fast "did stage-2 linker change?" check
 sha256sum out/target/product/shamu/system/bin/linker{,64}

 # e) Watchdog – kill hung jack-server / soong_ui very often
 alias kill-soong='pkill -9 -f "jack-server|soong_ui|ninja"'

 # f) Parallel extraction of super.img (very useful on shamu)
 lpunpack out/target/product/shamu/super.img extracted-partitions/
 lpmake --device-size=...   # rebuild super.img after manual changes

 # ────────────────────────────────────────────────
 #  git / repo discipline that saves pain later
 # ────────────────────────────────────────────────

 1. Never commit directly on lineage-22.0 / android-15.0 branch
 2. Use topic branches: lumen/treble-overlay-shamu, lumen/fix-camera-hal3, etc
 3. Use repo manifest tags / local_manifests/fragments/
 4. Keep device repo + kernel + vendor blobs in separate repos
 5. Use --depth=1 on kernel/vendor when possible
 6. git gc --aggressive --prune=now   (once every few months)

 # ────────────────────────────────────────────────
 #  Order of operations when you come back after 2 weeks
 # ────────────────────────────────────────────────

 0. git stash -u     (in every repo that has changes)
 1. repo sync -j6 --force-sync --no-tags
 2. ./lumen/scripts/apply-patches.sh   # or ./build/patch.sh
 3. source build/envsetup.sh
 4. lunch lumen_shamu-userdebug
 5. kill-soong
 6. m -j$(nproc --all) bootimage systemimage vendorimage productimage
 7. ./lumen/scripts/fastboot-flash-all.sh --skip userdata
Most time-efficient daily pattern in 2025–2026 for shamu-class devices:
repo sync -j5 --no-tags
source build/envsetup.sh
lunch lumen_shamu-userdebug
m -j$(nproc --all) bootimage systemimage productimage
./fastboot-flash-changed.sh
Pick only what you need — full m on shamu still takes 45–100 minutes even with ccache.
Anything you find yourself doing more than twice → script it.
Good luck with Lumen.
```
