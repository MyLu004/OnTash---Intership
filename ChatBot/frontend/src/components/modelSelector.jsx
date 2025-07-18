import { useState } from "react";

function ModelSelector({ selectedModel, setSelectedModel }) {
  const [open, setOpen] = useState(false);
  const models = ["GPT-3.5", "GPT-4", "LLaMA-3", "Mistral"];

  return (
    <div className="relative text-black mb-4 ">
      <button
        onClick={() => setOpen(!open)}
        className="bg-[var(--color-button)] text-[var(--color-text)] px-4 py-2 rounded-md shadow hover:bg-[var(--color-button-hover)] hover:text-black font-semibold"
      >
        {selectedModel || "Select Model"} ▼
      </button>
      {open && (
        <ul className="absolute left-0 mt-2 bg-[var(--color-accent)] border rounded-md shadow-lg z-10 w-2/12">
          {models.map((model) => (
            <li
              key={model}
              onClick={() => {
                setSelectedModel(model);
                setOpen(false);
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
