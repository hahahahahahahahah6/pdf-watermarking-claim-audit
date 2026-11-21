# Documentation claim auditor

An offline static auditor compares exact documentation claims with Python source patterns. It never executes inspected source. It scans the root README and Markdown under directories named docs, excluding fenced blocks; inline code counts. Normalization ignores case, expands contractions, replaces hyphens with spaces, and collapses whitespace. Denial spans are removed before positive matching.

```text
pdf-watermarking-claim-audit audit [repo] [--json] [--verbose] [--ignore PREFIX] [--fail-on high|medium]
python3 -m pdf_watermarking_claim_audit audit [repo]
documented-pdf-watermarking-claim-false
documented-no-pdf-watermarking-claim-false
```

The default failure threshold is high. A finding supported only by tests has medium severity. Exit status is 0 for pass, 2 for findings at the threshold, and 1 for usage or I/O errors. Ignore prefixes can be repeated. Source under fixtures, docs and examples is excluded; test files are reported separately. Symbolic links are excluded.

The exact matching phrases are:

```text
add watermark to pdf
adds watermark to pdf
adding watermark to pdf
add watermarks to pdf
adds watermarks to pdf
adding watermarks to pdf
watermark pdf
watermarks pdf
watermarking pdf
watermark pdfs
watermarks pdfs
watermarking pdfs
add watermark to pdfs
adds watermark to pdfs
adding watermark to pdfs
apply watermark to pdf
applies watermark to pdf
applying watermark to pdf
pdf watermark
pdf watermarks
pdf watermarking
watermark pdf document
watermarks pdf document
watermarking pdf document
watermark pdf file
watermarks pdf file
watermarking pdf file
add text watermark
adds text watermark
adding text watermark
add image watermark
adds image watermark
adding image watermark
stamp pdf
stamps pdf
stamping pdf
stamp watermark
stamps watermark
stamping watermark
watermark pdf page
watermarks pdf page
watermarking pdf page
insert watermark
inserts watermark
inserting watermark
add watermark to pdf file
adds watermark to pdf file
adding watermark to pdf file
watermark pdf pages
watermarks pdf pages
no pdf watermarking
does not add watermark to pdf
does not add watermarks to pdf
does not watermark pdf
does not watermark pdfs
does not add watermark to pdfs
does not apply watermark to pdf
does not watermark pdf document
does not watermark pdf file
does not add text watermark
does not add image watermark
does not stamp pdf
does not stamp watermark
does not watermark pdf page
does not insert watermark
does not add watermark to pdf file
no pdf watermark
does not support pdf watermarking
without pdf watermarking
pdf watermarking not supported
no pdf watermarking support
does not watermark pdf pages
pdf watermarking not available
no watermark pdf
```

## Limits

This phrase

```text
pdf watermarking
```

 may describe a roadmap item rather than an implemented feature.

This phrase

```text
pdf watermark
```

 may describe a setting that is only read from configuration.

This phrase

```text
add text watermark
```

 may refer to an image instead of a page.

This phrase

```text
add image watermark
```

 may refer to a photo instead of a page.

This phrase

```text
stamp watermark
```

 may refer to an image instead of a page.

This phrase

```text
insert watermark
```

 may refer to a video frame instead of a page.

This phrase

```text
stamp pdf
```

 may refer to a received-date stamp.

This phrase

```text
watermark pdf
```

 may describe a wrapper that never performs the operation.

A reader and an unrelated page merge in the same module count together.

An opener and an unrelated page overlay in the same module count together.

An opener and an unrelated rotated text insertion in the same module count together.

A page merger and an unrelated add call in the same module count together.

A merged page can be unrelated to the intended feature; its content is not examined.

An overlaid page can be a full page; its content is not examined.

Rotated text can be a header; its intent is not examined.

A page merger and add call count even without rendering.

An empty merged page dictionary still counts.

An empty inserted text string still counts.

A reader alone does not count.

A writer paired with a page merge does not count.

A page merge without a reader in the same module does not count.

A page overlay without an opener in the same module does not count.

Rotated text insertion without an opener in the same module does not count.

Plain text insertion without a rotation keyword does not count.

Text insertion with zero rotation does not count.

Text insertion with a variable rotation does not count.

Text insertion with rotation 45 does not count.

Image insertion alone does not count.

A page merger alone does not count.

An add call without a page merger in the same module does not count.

A page merger followed only by rendering does not count.

Legacy rotated and scaled merge wrappers are missed.

Creating an overlay using reportlab alone is missed.

The pikepdf library is missed; its checked wheel has no dedicated API for this feature.

A writer that appends or merges whole files is missed.

A writer that adds pages is missed.

A writer that encrypts is missed.

A reader or writer that rotates pages is missed.

An opener with a page rotation call is missed.

A writer that updates form fields is missed.

Calls to pyhanko or endesive to sign are missed.

A reader used solely for reading is missed.

Document generation operations alone are missed.

Whole-file merging operations alone are missed.

Splitting operations alone are missed.

Encryption operations alone are missed.

Rotation operations alone are missed.

Form filling operations alone are missed.

Extraction operations alone are missed.

Electronic signature operations alone are missed.

External qpdf, pdftk, and Ghostscript subprocesses are missed.

Mindee parsing with any product is missed.

Azure document analysis with any model is missed.

Veryfi calls of any kind are missed.

Google Document AI processing with any processor is missed.

Eden AI universal calls with any model are missed.

Textract calls of any kind are missed.

LlamaParse calls are missed.

Nanonets calls with opaque model identifiers are missed.

Docsumo uploads are missed.

ABBYY Vantage calls with opaque identifiers are missed.

Rossum calls with opaque identifiers are missed.

Klippa calls with opaque identifiers are missed.

Parseur calls with opaque identifiers are missed.

Extend calls with opaque identifiers are missed.

Hand-written raw dictionary and content stream edits are missed.

A detected operation does not prove visibility: opacity, colour, placement and layering are not assessed.

PDF extraction claims are outside the phrase lists.

PDF generation claims are outside the phrase lists.

PDF merging claims are outside the phrase lists.

PDF splitting claims are outside the phrase lists.

PDF encryption claims are outside the phrase lists.

PDF rotation claims are outside the phrase lists.

PDF form filling claims are outside the phrase lists.

spreadsheet reading claims are outside the phrase lists.

spreadsheet generation claims are outside the phrase lists.

Word document reading claims are outside the phrase lists.

Word document generation claims are outside the phrase lists.

presentation reading claims are outside the phrase lists.

presentation generation claims are outside the phrase lists.

table extraction claims are outside the phrase lists.

invoice extraction claims are outside the phrase lists.

receipt extraction claims are outside the phrase lists.

ID document extraction claims are outside the phrase lists.

bank check extraction claims are outside the phrase lists.

bank statement extraction claims are outside the phrase lists.

tax form extraction claims are outside the phrase lists.

pay stub extraction claims are outside the phrase lists.

health insurance card extraction claims are outside the phrase lists.

business card extraction claims are outside the phrase lists.

credit card extraction claims are outside the phrase lists.

contract extraction claims are outside the phrase lists.

mortgage extraction claims are outside the phrase lists.

resume extraction claims are outside the phrase lists.

bill of lading extraction claims are outside the phrase lists.

delivery note extraction claims are outside the phrase lists.

carte grise extraction claims are outside the phrase lists.

energy bill extraction claims are outside the phrase lists.

marriage certificate extraction claims are outside the phrase lists.

bank account details extraction claims are outside the phrase lists.

nutrition facts label extraction claims are outside the phrase lists.

material certificate extraction claims are outside the phrase lists.

US mail extraction claims are outside the phrase lists.

invoice splitter claims are outside the phrase lists.

multi-receipts detection claims are outside the phrase lists.

French health card extraction claims are outside the phrase lists.

Indian passport extraction claims are outside the phrase lists.

driver license extraction claims are outside the phrase lists.

vaccination card extraction claims are outside the phrase lists.

document cropping claims are outside the phrase lists.

image rotation claims are outside the phrase lists.

e-signature claims are outside the phrase lists.

payment processing claims are outside the phrase lists.

OCR claims are outside the phrase lists.

Static patterns do not judge semantics. Dead code counts. Alias chains the tracer cannot follow are missed. Only exact phrases match. Denials depend on the listed phrases. Each paired route must occur in one module.
