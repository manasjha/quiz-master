import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc } from "firebase/firestore";
import fs from "fs";
import csvParser from "csv-parser";

// Firebase Config
const firebaseConfig = {
  apiKey: "AIzaSyDk3BMLce4p0fr4ZvzOi1Idr8nhTrzu-gg",
  authDomain: "quiz-master-a925f.firebaseapp.com",
  projectId: "quiz-master-a925f",
  storageBucket: "quiz-master-a925f.firebasestorage.app",
  messagingSenderId: "655327292809",
  appId: "1:655327292809:web:c5c899fa6ffdf5cb30c558",
  measurementId: "G-0KZR3KH4X4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const uploadQuestions = async () => {
  fs.createReadStream("questions.csv")
    .pipe(csvParser())
    .on("data", (row) => {
      console.log("🔍 Checking row:", row); // Debugging

      // Debug: Log each individual field to see what's undefined
      console.log(`👉 Question: "${row["Question"]}"`);
      console.log(`👉 Option A: "${row["Option A"]}"`);
      console.log(`👉 Option B: "${row["Option B"]}"`);
      console.log(`👉 Option C: "${row["Option C"]}"`);
      console.log(`👉 Option D: "${row["Option D"]}"`);
      console.log(`👉 Correct Answer: "${row["Answer Option"]}"`);
      console.log(`👉 Year: "${row["Year"]}"`);
      console.log(`👉 Difficulty: "${row["Difficulty"]}"`);
      console.log(`👉 Topic: "${row["Topic"]}"`);
      console.log(`👉 Explanation: "${row["Explanation"]}"`);

      if (!row["Question"] || !row["Option A"] || !row["Answer Option"]) {
        console.warn("⚠️ Skipping row due to missing data:", row);
        return; // Skip empty rows
      }

      const formattedQuestion = {
        question: row["Question"].trim(),
        options: [row["Option A"], row["Option B"], row["Option C"], row["Option D"]],
        correctOption: row["Answer Option"].trim(),
        explanation: row["Explanation"]?.trim() || "No explanation provided",
        topic: row["Topic"]?.trim() || "General",
        difficulty: row["Difficulty"]?.trim() || "Medium",
        year: Number(row["Year"]) || 2024
      };

      console.log("✅ Ready to Upload:", formattedQuestion);
    })
    .on("end", async () => {
      console.log("🎉 CSV Processing Done!");
    });
};

uploadQuestions();
