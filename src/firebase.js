// Import Firebase SDKs
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore"; // Import Firestore

// Your Firebase Config
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
const db = getFirestore(app); // Initialize Firestore

export { db }; // Export Firestore instance
