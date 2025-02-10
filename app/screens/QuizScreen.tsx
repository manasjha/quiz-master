import React, { useEffect, useState } from "react";
import { View, Text, TouchableOpacity, FlatList, StyleSheet, Modal, Dimensions } from "react-native";
import { db } from "../../src/firebase";
import { collection, getDocs } from "firebase/firestore";
import { Ionicons } from "@expo/vector-icons";

const SCREEN_WIDTH = Dimensions.get("window").width;

const QuizScreen = ({ navigation }) => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [correctAnswer, setCorrectAnswer] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [explanationText, setExplanationText] = useState("");

  useEffect(() => {
    navigation.setOptions({ title: "Quiz: Polity" });

    const fetchQuestions = async () => {
      try {
        const querySnapshot = await getDocs(collection(db, "questions"));
        const questionList = querySnapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }));
        setQuestions(questionList);
      } catch (error) {
        console.error("Error fetching questions: ", error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [navigation]);

  const handleAnswerSelect = (option, optionIndex) => {
    if (selectedAnswer !== null) return; // Prevent multiple selections

    const correctOptionLetter = questions[currentQuestionIndex].correctOption;
    const selectedOptionLetter = String.fromCharCode(65 + optionIndex); // Convert index to A, B, C, D

    setSelectedAnswer(selectedOptionLetter);
    setCorrectAnswer(correctOptionLetter);

    // Highlight correct answer & auto move to next question
    const skipTime = selectedOptionLetter === correctOptionLetter ? 1500 : 3000;
    setTimeout(() => {
      handleNextQuestion();
    }, skipTime);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setSelectedAnswer(null);
      setCorrectAnswer(null);
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      alert("Quiz Finished!");
    }
  };

  const handleShowExplanation = () => {
    const explanation = questions[currentQuestionIndex].explanation || "No explanation provided.";
    setExplanationText(`Answer: ${questions[currentQuestionIndex].correctOption}\n\n${explanation}`);
    setModalVisible(true);
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <Text>Loading questions...</Text>
      </View>
    );
  }

  if (questions.length === 0) {
    return (
      <View style={styles.centered}>
        <Text>No questions found.</Text>
      </View>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];

  return (
    <View style={styles.container}>
      {/* Question Section (Top 50%) */}
      <View style={styles.questionContainer}>
        <Text style={styles.question}>{currentQuestion.question.replace(/\(A\).*$/, "").trim()}</Text>
      </View>

      {/* Options Section (Bottom 50%) */}
      <View style={styles.optionsContainer}>
        <FlatList
          data={currentQuestion.options}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item, index }) => {
            const isCorrect = String.fromCharCode(65 + index) === correctAnswer;
            const isSelected = String.fromCharCode(65 + index) === selectedAnswer;

            return (
              <TouchableOpacity
                style={[
                  styles.option,
                  isSelected && { backgroundColor: isCorrect ? "#2E7D32" : "#D32F2F" },
                  !isSelected && isCorrect && { backgroundColor: "#2E7D32" }
                ]}
                onPress={() => handleAnswerSelect(item, index)}
                disabled={selectedAnswer !== null} // Disable after selecting
              >
                <Text style={styles.optionText}>{item}</Text>
              </TouchableOpacity>
            );
          }}
        />

        {/* Bottom Buttons (Transparent Skip & Info) */}
        <View style={styles.bottomButtons}>
          {/* Explanation Button */}
          <TouchableOpacity style={styles.transparentButton} onPress={handleShowExplanation}>
            <Ionicons name="information-circle-outline" size={28} color="#E0E0E0" />
          </TouchableOpacity>

          {/* Skip Button */}
          <TouchableOpacity style={styles.transparentButton} onPress={handleNextQuestion}>
            <Ionicons name="refresh" size={28} color="#E0E0E0" />
          </TouchableOpacity>
        </View>
      </View>

      {/* Explanation Modal */}
      <Modal
        animationType="fade"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalContent}>
            <Text style={styles.modalText}>{explanationText}</Text>
            <TouchableOpacity onPress={() => setModalVisible(false)} style={styles.closeButton}>
              <Text style={styles.closeButtonText}>Close</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#121212", paddingHorizontal: 20 },
  centered: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "#121212" },

  questionContainer: { flex: 1, justifyContent: "center" },
  question: { 
    fontSize: 20, 
    fontWeight: "bold", 
    color: "#E0E0E0", 
    textAlign: "center", 
    fontFamily: "Roboto",
    lineHeight: 28 // Even spacing
  },

  optionsContainer: { flex: 1, justifyContent: "flex-end", paddingBottom: 30 },
  option: { padding: 15, borderRadius: 8, marginBottom: 10, borderWidth: 1, borderColor: "#E0E0E0", backgroundColor: "#282828" },
  optionText: { fontSize: 16, color: "#E0E0E0" },

  bottomButtons: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginTop: 20 },

  transparentButton: { 
    width: 50, 
    height: 50, 
    borderRadius: 25, 
    justifyContent: "center", 
    alignItems: "center",
    backgroundColor: "transparent" // Fully transparent button
  },

  modalContainer: { flex: 1, justifyContent: "center", alignItems: "center", backgroundColor: "rgba(0,0,0,0.7)" },
  modalContent: { width: SCREEN_WIDTH * 0.8, backgroundColor: "#282828", padding: 20, borderRadius: 10 },
  modalText: { fontSize: 18, color: "#E0E0E0", textAlign: "center", marginBottom: 10 },
  closeButton: { backgroundColor: "#D32F2F", padding: 10, borderRadius: 5, alignItems: "center" },
  closeButtonText: { color: "#FFFFFF", fontWeight: "bold" },
});

export default QuizScreen;
