pub mod backend;
pub mod corpus;
pub mod model;
pub mod scheduler;
pub mod store;
use std::sync::{Arc, Mutex};
use tauri::Manager;
type Shared = Arc<Mutex<backend::Backend>>;

#[tauri::command]
async fn api(
    app: tauri::AppHandle,
    state: tauri::State<'_, Shared>,
    command: String,
    payload: Option<serde_json::Value>,
) -> Result<serde_json::Value, String> {
    let shared = state.inner().clone();
    tauri::async_runtime::spawn_blocking(move || {
        if command == "pick_corpus" {
            let chosen = rfd::FileDialog::new()
                .set_title("Select Physica corpus folder")
                .pick_folder();
            return match chosen {
                Some(path) => shared.lock().map_err(|e| e.to_string())?.choose_root(path),
                None => Ok(serde_json::Value::Null),
            };
        }
        let mut b = shared.lock().map_err(|e| e.to_string())?;
        let result = b.dispatch(&command, payload.unwrap_or(serde_json::json!({})))?;
        if command == "document" {
            if let Some(path) = result["path"].as_str() {
                app.asset_protocol_scope()
                    .allow_file(path)
                    .map_err(|e| e.to_string())?;
            }
        }
        Ok(result)
    })
    .await
    .map_err(|e| e.to_string())?
}
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            // Optional local profile override is useful for portable testing. Normal installs use Tauri's app-data directory.
            let dir = std::env::var_os("PHYSICA_STATE_DIR")
                .map(std::path::PathBuf::from)
                .unwrap_or(app.path().app_data_dir()?);
            let b = backend::Backend::new(dir.join("physica_state.sqlite"))
                .map_err(std::io::Error::other)?;
            app.manage(Arc::new(Mutex::new(b)));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![api])
        .run(tauri::generate_context!())
        .expect("Physica failed to launch");
}
