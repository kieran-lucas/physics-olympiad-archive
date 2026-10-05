//! Read-only corpus check using the production adapter and an automatically removed scratch state DB.
fn main() {
    let profile = tempfile::tempdir().expect("scratch profile");
    let mut backend = physica_lib::backend::Backend::new(profile.path().join("state.sqlite"))
        .expect("initialize Physica scratch state");
    backend.index(true).expect("normalize local corpus");
    println!(
        "{}",
        serde_json::to_string_pretty(&backend.diagnostics().expect("diagnostics")).unwrap()
    );
}
