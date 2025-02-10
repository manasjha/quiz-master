import { initializeApp } from "firebase/app";
import { getFirestore, collection, addDoc } from "firebase/firestore";
import fs from "fs";
import csvParser from "csv-parser";

// 🔥 Firebase Config
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

// 📌 CSV File Path
const csvFilePath = "./questions.csv";

// ✅ Check if CSV file exists
if (!fs.existsSync(csvFilePath)) {
  console.error("❌ ERROR: 'questions.csv' not found! Place it in the same folder as upload_questions.js.");
  process.exit(1);
} else {
  console.log("✅ Found 'questions.csv'! Proceeding with upload...");
}

// 🚀 Upload Questions Function
const uploadQuestions = async () => {
  const questions = [];

  fs.createReadStream(csvFilePath)
    .pipe(csvParser())
    .on("data", (row) => {
      console.log("\n🔍 Checking row:", row);

      // Debug: Log each field
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

      // 🛑 Skip invalid rows (empty or missing required fields)
      if (!row["Question"] || !row["Option A"] || !row["Answer Option"]) {
        console.warn("⚠️ Skipping row due to missing data:", row);
        return;
      }

      // ✅ Format question properly
      const formattedQuestion = {
        question: row["Question"].replace(/^\d+\.\s*/, "").trim(), // Remove leading numbers like "70."
        options: [row["Option A"], row["Option B"], row["Option C"], row["Option D"]],
        correctOption: row["Answer Option"].trim(),
        explanation: row["Explanation"]?.trim() || "No explanation provided",
        topic: row["Topic"]?.trim() || "General",
        difficulty: row["Difficulty"]?.trim() || "Medium",
        year: Number(row["Year"]) || 2024
      };

      console.log("✅ Ready to Upload:", formattedQuestion);
      questions.push(formattedQuestion);
    })
    .on("end", async () => {
      console.log("\n🚀 Uploading Questions to Firestore...");
      
      for (const question of questions) {
        try {
          await addDoc(collection(db, "questions"), question);
          console.log(`✅ Uploaded: ${question.question}`);
        } catch (error) {
          console.error("❌ Error uploading:", question.question, error);
        }
      }

      console.log("\n🎉 ALL QUESTIONS UPLOADED SUCCESSFULLY! 🎉");
    });
};

// Run the upload function
uploadQuestions();
