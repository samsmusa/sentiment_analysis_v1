import React from "react";
import { useSentiment } from "../../../common/sentimentContext";

export default function Form() {
  const { setSentiment } = useSentiment();
  const debounceOnChange = React.useCallback(debounce(onChange, 700), []);

  function onChange(value) {
    if (value) {
      fetch(`/api/sentiment`, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "cors", // no-cors, *cors, same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: value }),
      })
        .then((res) => res.json())
        .then((res) => setSentiment(res));
    } else {
      setSentiment({ sentiment: "neutral", value: 0 });
    }
  }
  function debounce(func, wait) {
    let timeout;
    return function (...args) {
      const context = this;
      if (timeout) clearTimeout(timeout);
      timeout = setTimeout(() => {
        timeout = null;
        func.apply(context, args);
      }, wait);
    };
  }
  return (
    <form>
      <div class="w-full mb-4 border border-green-500 rounded-lg bg-black">
        <div class="flex items-center justify-between px-3 py-2 border-b dark:border-gray-600"></div>
        <div class="px-4 py-2 bg-black rounded-b-lg dark:bg-gray-800">
          <textarea
            onChange={(e) => debounceOnChange(e.target.value)}
            id="editor"
            rows="8"
            style={{ backgroundColor: "black" }}
            class="block w-full px-0 text-sm text-green-500 bg-black border-0 dark:bg-gray-800 focus:ring-0 dark:text-white dark:placeholder-gray-400"
            placeholder="Write something..."
            required
          ></textarea>
        </div>
      </div>
    </form>
  );
}
