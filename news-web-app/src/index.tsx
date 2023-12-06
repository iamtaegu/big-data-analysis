import './index.css';

import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { BrowserRouter } from "react-router-dom";

import { store } from './app/store';

import App from "./App";

import { initializeApp } from "firebase/app";
import { getAnalytics, logEvent } from "firebase/analytics";

const firebaseConfig = {
    apiKey: "AIzaSyB8IplvZa_X4NbM5X3Crv9CmW2xvlMFqWk",
    authDomain: "news-trends-e161e.firebaseapp.com",
    projectId: "news-trends-e161e",
    storageBucket: "news-trends-e161e.appspot.com",
    messagingSenderId: "376081045163",
    appId: "1:376081045163:web:d67f920357b304ba6909ee",
    measurementId: "G-6JLTS5MXPF"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

logEvent(analytics, 'web_app_starts');

const root = ReactDOM.createRoot(
    document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>
        <Provider store={store} >
            <BrowserRouter>
                <App />
            </BrowserRouter>
        </Provider>
    </React.StrictMode>
);

