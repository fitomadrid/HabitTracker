import axios from 'axios';
require('dotenv').config();

const API_BASE_URL = process.env.REACT_APP_API_URL;

async function retrieveHabitsFromServer() {
  try {
    const response = await axios.get(`${API_BASE_URL}/habits`);
    renderHabitsToDOM(response.data);
  } catch (error) {
    console.error("Error retrieving habits:", error);
  }
}

function renderHabitsToDOM(habitsList) {
  const habitsListContainer = document.getElementById('habits-container');
  habitsListContainer.innerHTML = '';
  habitsList.forEach(habit => {
    const habitDiv = document.createElement('div');

    const habitNameSpan = document.createElement('span'); // For the habit name
    habitNameSpan.textContent = habit.name;
    habitDiv.appendChild(habitNameSpan);

    const habitEditButton = document.createElement('button'); // For editing habit
    habitEditButton.textContent = 'Edit';
    habitEditButton.onclick = function() {
      const newHabitName = prompt('Enter new habit name', habit.name);
      if (newHabitName) {
        updateExistingHabit(habit.id, { name: newHabitName });
      }
    };
    habitDiv.appendChild(habitEditButton);

    const habitDeleteButton = document.createElement('button'); // For deleting habit
    habitDeleteButton.textContent = 'Delete';
    habitDeleteButton.onclick = function() {
      removeHabitById(habit.id);
    };
    habitDiv.appendChild(habitDeleteButton);

    habitsListContainer.appendChild(habitDiv);
  });
}

async function submitNewHabit(habitDetails) {
  try {
    await axios.post(`${API_BASE_URL}/habits`, habitDetails);
    retrieveHabitsFromServer(); // Refresh the list
  } catch (error) {
    console.error("Error submitting new habit:", error);
  }
}

async function updateExistingHabit(habitId, habitUpdates) {
  try {
    await axios.put(`${API_BASE_URL}/habits/${habitId}`, habitUpdates);
    retrieveHabitsFromServer(); // Refresh the list
  } catch (error) {
    console.error("Error updating habit:", error);
  }
}

async function removeHabitById(habitId) {
  try {
    await axios.delete(`${API_BASE_URL}/habits/${habitId}`);
    retrieveHabitsFromServer(); // Refresh the list
  } catch (error) {
    console.error("Error removing habit:", error);
  }
}

function attachEventListenersToForms() {
  document.getElementById('add-habit-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const newHabitDetails = {
      name: e.target.elements.name.value,
    };
    submitNewHabit(newHabitDetails);
  });
}

function initializeHabitTrackerApp() {
  retrieveHabitsFromServer();
  attachEventListenersToForms();
}

window.onload = initializeHabitTrackerApp;