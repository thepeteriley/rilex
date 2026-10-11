# Supplemental installed-system screen-lock test

On 2026-10-11, the preserved disposable installed disk from the older `d642` diagnostic candidate (`.cache/qa-install.qcow2`, with `.cache/qa-uefi/vars.fd`) booted independently without an attached ISO under QEMU q35/qemu64, two TCG virtual CPUs and 4 GiB memory. The normal account logged in through SDDM using the private mode-0600 QA credential fixture. Credentials were entered through `tests/qa-private-keyboard.py`; their values were neither command arguments nor log output.

Observed result: **PASS**. Super+Escape changed the working Hyprland desktop to the Rilex Hyprlock screen. Entering the correct account password and submitting Return restored the same desktop. Screenshots are retained under ignored `.cache/qa-lock-test`: `03-login.png`, `04-desktop.png`, `05-lock.png`, and `06-unlock.png`.

The installed executable reported `Hyprlock version v0.9.6` (`09-version.png`). The installed `/etc/xdg/hypr/hyprlock.conf` checksum (`08-provenance.png`) was:

```text
c686b52331b133c6d3a5ef3bda5e3644a9657b6907311a83c146a7e7af23d748
```

Independent extraction from the final `feaca7002cb46eb391b0cf40fc5615a09be1d231` defaults package found that exact same configuration checksum, and its manifest records the same Hyprlock `0.9.6-1~bpo13+1` package. This test supplements final-candidate QA; it is not an installation or boot test of the final ISO. The old disk predates packaged `build-info` and has known older desktop defects. The password field outline was not visible in the old TCG-rendered lock screenshot, although password authentication and restoration worked. Wrong-password rejection, suspend/resume locking and physical laptop rendering were not tested here.
