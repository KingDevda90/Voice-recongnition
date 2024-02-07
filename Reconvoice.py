import streamlit as st
import speech_recognition as sr


def transcribe_speech(selected_api, selected_language, is_paused):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        st.info("Parlez maintenant...")

        # Pause/Resume functionality
        if is_paused:
            st.warning("Enregistrement en pause. Cliquez sur 'Reprendre' pour continuer.")
            st.stop()

        audio_text = r.listen(source)
        st.info("Transcription en cours...")

        try:
            if selected_api == "Google":
                text = r.recognize_google(audio_text, language=selected_language)
            elif selected_api == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=selected_language)
            # Ajoutez d'autres options selon les APIs disponibles dans la bibliothèque SpeechRecognition

            return text
        except sr.UnknownValueError:
            return "Désolé, je n'ai pas compris ce que vous avez dit. Veuillez réessayer."
        except sr.RequestError as e:
            if "Google" in selected_api:
                return f"Erreur lors de la requête vers le service de reconnaissance vocale Google ; {e}"
            elif "Sphinx" in selected_api:
                return f"Erreur lors de la reconnaissance vocale avec Sphinx ; {e}"
            # Ajoutez d'autres options selon les APIs disponibles dans la bibliothèque SpeechRecognition
            else:
                return f"Erreur lors de la reconnaissance vocale avec {selected_api} ; {e}"


def save_to_file(text):
    filename = "transcription.txt"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    st.success(f"Transcription enregistrée dans le fichier {filename}")


def main():
    st.title("Application de Reconnaissance Vocale")

    # Ajoutez une liste déroulante pour sélectionner l'API
    selected_api = st.selectbox("Sélectionnez l'API de Reconnaissance Vocale", ["Google", "Sphinx"])

    # Ajoutez une liste déroulante pour sélectionner la langue
    selected_language = st.selectbox("Sélectionnez la langue", ["en-US", "fr-FR"])

    # Ajoutez un bouton pour la pause/reprise
    is_paused = st.session_state.get("is_paused", False)
    if st.button("Pause/Reprendre"):
        st.session_state.is_paused = not is_paused

    st.write("Cliquez sur le microphone pour commencer à parler :")

    if st.button("Commencer l'enregistrement"):
        text = transcribe_speech(selected_api, selected_language, is_paused)
        st.write("Transcription : ", text)

        # Ajoutez un bouton pour enregistrer la transcription dans un fichier
        if st.button("Enregistrer dans un fichier"):
            save_to_file(text)


if __name__ == "__main__":
    main()

