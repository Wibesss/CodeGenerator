import React, { useState } from "react";
import axios from "axios";

function CodeGenerator() {
  const [inputCode, setInputCode] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/generate", {
        input_code: inputCode,
      });
      setGeneratedCode(response.data.generated_code);
    } catch (error) {
      console.error("Error generating code:", error);
    }
  };

  return (
    <div>
      <h1>Code Generator</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={inputCode}
          onChange={(e) => setInputCode(e.target.value)}
          rows="6"
          cols="60"
          placeholder="Enter code to complete"
        />
        <br />
        <button type="submit">Generate</button>
      </form>

      <h2>Generated Code</h2>
      <textarea
        value={generatedCode}
        readOnly
        rows="6"
        cols="60"
        placeholder="Generated code will appear here"
      />
    </div>
  );
}

export default CodeGenerator;
