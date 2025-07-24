import { useState } from "react";

function ModelSelector({ selectedModel, setSelectedModel }) {
  // state to track whether the dropdown menu is open
  const [open, setOpen] = useState(false);

  // list of available AI models to choose from
  const models = ["GPT-3.5", "GPT-4", "LLaMA-3", "Mistral"];

  return (
    <div className="relative text-black mb-4 ">

      {/* Button to toggle the model dropdown */}
      <button
        onClick={() => setOpen(!open)}
        className="bg-[var(--color-button)] text-[var(--color-text)] px-4 py-2 rounded-md shadow hover:bg-[var(--color-button-hover)] hover:text-black font-semibold"
      >
        {selectedModel || "Select Model"} ▼
      </button>
      
      {/* Dropdown menu with model options */}
      {open && (
        <ul className="absolute left-0 mt-2 bg-[var(--color-accent)] border rounded-md shadow-lg z-10 w-2/12">
          {models.map((model) => (
            <li
              key={model}
              onClick={() => {
                setSelectedModel(model);  // update selected model in parent
                setOpen(false);           // close dropdown
              }}
              className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
            >
              {model}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default ModelSelector;
