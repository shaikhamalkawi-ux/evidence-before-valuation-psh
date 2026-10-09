# Zenodo archival release plan

Do **not** archive this repository in Zenodo until the public release contents and license have been checked.

Recommended sequence:

1. Confirm that all repository files are publication-safe.
2. Select the final public license.
3. Tag the repository release (recommended first archival tag: `v1.0.0`).
4. Connect the public GitHub repository to Zenodo.
5. Archive the GitHub release in Zenodo.
6. Record the Zenodo DOI in:
   - `README.md`
   - `CITATION.cff`
   - the manuscript Data and Code Availability statement.

The Zenodo DOI should identify the immutable archival release. GitHub remains the development repository.

## License decision still required

A license has intentionally not yet been committed because the authors should explicitly choose the public licensing terms.

A practical option is:
- MIT for original code; and
- a separate data/documentation notice for derived AEMO material with AEMO attribution requirements.

Do not publish confidential or non-redistributable third-party material.
