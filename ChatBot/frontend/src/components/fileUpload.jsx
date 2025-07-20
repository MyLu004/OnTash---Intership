import { useRef } from "react";

function FileUpload({ onFileUpload }) {
  const fileInputRef = useRef();

  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      onFileUpload(file); // pass file to parent
    }
  };

  return (
    <div className="my-2">
      <button
        className="px-4 py-2 bg-white text-black rounded-md font-semibold hover:bg-gray-100"
        onClick={() => fileInputRef.current.click()}
      >
        Upload File 📎
      </button>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleChange}
        accept=".pdf,image/*"
        className="hidden"
      />
    </div>
  );
}

export default FileUpload;
