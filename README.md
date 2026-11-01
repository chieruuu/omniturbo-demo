# OmniTurbo Supplementary Videos

## View the videos

Open the **Website** link in the upper-right corner of this page to view and play the supplementary videos. The `index.html` file shown in the repository browser is a source file view; use **Website** to open the playable gallery.

If the Website link is not visible, open the anonymous project page and choose **View page** from the project menu.

- Sparse Attention Comparison: 22 selected cases, each retaining all four settings (88 videos).
- Human Motion and Performance: Garden tai chi, Contemporary dance, Drummer performance (3 videos).
- Joint Audio–Video Generation: 8 landscape-format examples.
- Speech Editing: LTX-2.3 vs. OmniTurbo: 27 cases, each with source video and two methods (81 videos), grouped by deletion, insertion, and replacement.

180 videos in total. Original prompts are shown where supplied; operation-level editing instructions are labeled separately from unavailable exact target transcripts. Retake clips come from `official_vs_our_retake36`; LTX-2.3 baseline files are remuxed and OmniTurbo files are encoded to browser-compatible H.264 CRF 18 at original resolution, preserving the supplied audio. No changes are made to source artifacts.

The gallery is a qualitative selection after reviewing temporal samples, not the full benchmark or a quantitative quality assessment.

Source/conditioned-input videos and posters are restored byte-for-byte from the original site commit `2089e17`, matched by retake case ID. The source is the model conditioning input, distinct from the LTX-2.3 baseline output.
