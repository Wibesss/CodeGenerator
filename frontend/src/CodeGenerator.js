import React, { useState } from "react";
import axios from "axios";

function CodeGenerator() {
  const [inputCode, setInputCode] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");
  const [loadingCode, setLoadingCode] = useState(false);
  const [chooseStrongModel, setChooseStrongModel] = useState(true);

  const apiStrong = "http://127.0.0.1:5000";
  const apiWeak = "http://127.0.0.1:5001";

  const handleGenerateBlock = async (e) => {
    if (inputCode === "") return alert("Write some code as input first");

    e.preventDefault();
    setLoadingCode(true);
    try {
      const response = await axios.post(
        `${chooseStrongModel ? apiStrong : apiWeak}/generate`,
        {
          input_code: inputCode,
        }
      );
      setGeneratedCode(response.data.generated_code);
    } catch (error) {
      console.error("Error generating code:", error);
    } finally {
      setLoadingCode(false);
    }
  };

  const handleAutocomplete = async (e) => {
    if (inputCode === "") return alert("Write some code as input first");

    e.preventDefault();
    setLoadingCode(true);
    try {
      const response = await axios.post(
        `${chooseStrongModel ? apiStrong : apiWeak}/autocompleateline`,
        {
          input_code: inputCode,
        }
      );
      setGeneratedCode(response.data.generated_code);
    } catch (error) {
      console.error("Error generating code:", error);
    } finally {
      setLoadingCode(false);
    }
  };

  const handleNextLine = async (e) => {
    if (inputCode === "") return alert("Write some code as input first");

    e.preventDefault();
    setLoadingCode(true);
    try {
      const response = await axios.post(
        `${chooseStrongModel ? apiStrong : apiWeak}/generatenextline`,
        {
          input_code: inputCode,
        }
      );
      setGeneratedCode(response.data.generated_code);
    } catch (error) {
      console.error("Error generating code:", error);
    } finally {
      setLoadingCode(false);
    }
  };

  const handleToggleModel = () => {
    setChooseStrongModel((prev) => !prev);
  };

  return (
    <div className="flex flex-col h-full w-4/5 justify-center">
      <h1 className="text-5xl text-blue-500 m-2 font-bold">Code Generator</h1>
      <textarea
        className="bg-slate-600 text-2xl p-2 font-semibold h-1/4 text-slate-300 resize-none"
        value={inputCode}
        onChange={(e) => setInputCode(e.target.value)}
        rows="6"
        cols="60"
        spellCheck={false}
        placeholder="Enter your code"
      />
      <div className="flex flex-row">
        <div className="flex flex-row w-4/5">
          <button className="btn-prim" onClick={handleGenerateBlock}>
            Generate
          </button>
          <button className="btn-prim" onClick={handleAutocomplete}>
            Autocomplete Line
          </button>
          <button className="btn-prim" onClick={handleNextLine}>
            Generate Next Line Only
          </button>
        </div>
        <div className="w-1/5 flex justify-end">
          <button className="btn-prim ml-2" onClick={handleToggleModel}>
            Switch to {chooseStrongModel ? "Weak" : "Strong"} Model
          </button>
        </div>
      </div>

      <h2 className="text-5xl text-blue-500 m-2 font-bold">Generated Code</h2>
      <textarea
        className="bg-slate-600 text-2xl p-2 font-semibold h-2/4 text-slate-300 resize-none"
        value={loadingCode ? "Generating code..." : generatedCode}
        readOnly
        rows="6"
        cols="60"
        placeholder={
          loadingCode ? "Generating code..." : "Generated code will appear here"
        }
      />
    </div>
  );
}

export default CodeGenerator;
