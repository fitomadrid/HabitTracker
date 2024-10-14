import axios from 'axios';
require('dotenv').config();
const BASE_URL = process.env.REACT_APP_API_URL;
async function fetchHabits() {
  try {
    const response = await axios.get(`${BASE_URL}/habits`);
    displayHabits(response.data);
  } catch (error) {
    console.error("Error fetching habits:", error);
  }
}
function displayHabits(habits) {
  const habitsContainer = document.getElementById('habits-container');
  habitsContainer.innerHTML = '';
  habits.forEach(habit => {
    const habitElement = document.createElement('div');
    habitElement.textContent = habit.name;
    habitsContainer.appendChild(habitElement);
  });
}
async function addHabit(habitData) {
  try {
    await axios.post(`${BASE_URL}/habits`, habitData);
    fetchHabits();
  } catch (error) {
    console.error("Error adding habit:", error);
  }
}
async function updateHabit(id, updatedData) {
  try {
    await axios.put(`${BASE_URL}/habits/${id}`, updatedData);
    fetchHabits();
  } catch (error) {
    console.error("Error updating habit:", error);
  }
}
async function deleteHabit(id) {
  try {
    await axios.delete(`${BASE_URL}/habits/${id}`);
    fetchHabits();
  } catch (error) {
    console.error("Error deleting habit:", error);
  }
}
function setupEventListeners() {
  document.getElementById('add-habit-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const habitData = {
      name: e.target.elements.name.value,
    };
    addHabit(habitData);
  });
}
function initApp() {
  fetchHabits();
  setupEventListeners();
}
window.onload = initApp;