import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
from datetime import datetime
import json
import re
import string

class Keylogger:
        def __init__(self, root):
            self.root = root
            self.root.title("KeyLogger Simulator")
            self.root.geometry("1000x700")
            
            # Data storage
            self.keystroke_log = []
            self.word_log = []
            self.current_word = ""
            self.start_time = None
            self.char_count = 0
            
            # Dictionary features
            self.common_words = self.load_common_words()
            self.typed_words = []
            self.correct_words = 0
            self.incorrect_words = 0
            
            self.setup_ui()
            
        def load_common_words(self):
            """Load a basic set of common English words"""
            common_words = {
                'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with',
                'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
                'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up',
                'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time',
                'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could',
                'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think',
                'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even',
                'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us', 'is', 'water', 'long',
                'find', 'here', 'thing', 'great', 'man', 'world', 'life', 'still', 'public', 'human', 'read',
                'keep', 'eye', 'never', 'last', 'door', 'between', 'city', 'tree', 'cross', 'since', 'hard',
                'start', 'might', 'story', 'saw', 'far', 'sea', 'draw', 'left', 'late', 'run', 'while', 'press',
                'close', 'night', 'real', 'book', 'took', 'science', 'eat', 'room', 'friend', 'began', 'idea',
                'fish', 'mountain', 'north', 'once', 'base', 'hear', 'horse', 'cut', 'sure', 'watch', 'color',
                'face', 'wood', 'main', 'enough', 'plain', 'girl', 'usual', 'young', 'ready', 'above', 'ever',
                'red', 'list', 'though', 'feel', 'talk', 'bird', 'soon', 'body', 'dog', 'family', 'direct',
                'leave', 'song', 'measure', 'state', 'product', 'black', 'short', 'numeral', 'class', 'wind',
                'question', 'happen', 'complete', 'ship', 'area', 'half', 'rock', 'order', 'fire', 'south',
                'problem', 'piece', 'told', 'knew', 'pass', 'farm', 'top', 'whole', 'king', 'size', 'heard',
                'best', 'hour', 'better', 'during', 'hundred', 'am', 'remember', 'step', 'early', 'hold',
                'west', 'ground', 'interest', 'reach', 'fast', 'five', 'sing', 'listen', 'six', 'table',
                'travel', 'less', 'morning', 'ten', 'simple', 'several', 'vowel', 'toward', 'war', 'lay',
                'against', 'pattern', 'slow', 'center', 'love', 'person', 'money', 'serve', 'appear', 'road',
                'map', 'science', 'rule', 'govern', 'pull', 'cold', 'notice', 'voice', 'fall', 'power', 'town',
                'fine', 'certain', 'fly', 'unit', 'lead', 'cry', 'dark', 'machine', 'note', 'wait', 'plan',
                'figure', 'star', 'box', 'noun', 'field', 'rest', 'correct', 'able', 'pound', 'done', 'beauty',
                'drive', 'stood', 'contain', 'front', 'teach', 'week', 'final', 'gave', 'green', 'oh', 'quick',
                'develop', 'sleep', 'warm', 'free', 'minute', 'strong', 'special', 'mind', 'behind', 'clear',
                'tail', 'produce', 'fact', 'street', 'inch', 'lot', 'nothing', 'course', 'stay', 'wheel',
                'full', 'force', 'blue', 'object', 'decide', 'surface', 'deep', 'moon', 'island', 'foot',
                'yet', 'busy', 'test', 'record', 'boat', 'common', 'gold', 'possible', 'plane', 'age',
                'dry', 'wonder', 'laugh', 'thousands', 'ago', 'ran', 'check', 'game', 'shape', 'yes', 'hot',
                'miss', 'brought', 'heat', 'snow', 'bed', 'bring', 'sit', 'perhaps', 'fill', 'east', 'weight',
                'language', 'among','hi','hello','love','hate','vaishal','shah','hemil','soni','aakash','darshan','darshit','priyal','krisha','patel'
            }
            return common_words
            
        def setup_ui(self):
            # Main frame
            main_frame = ttk.Frame(self.root, padding="10")
            main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Title
            title_label = ttk.Label(main_frame, text="KeyLogger", 
                                font=("Arial", 16, "bold"))
            title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
            
            # Instructions
            instructions = ttk.Label(main_frame, 
                                    text="Type in the text area below. The system will analyze your words and provide dictionary feedback.",
                                    font=("Arial", 10))
            instructions.grid(row=1, column=0, columnspan=3, pady=(0, 10))
            
            # Text area for typing
            text_frame = ttk.LabelFrame(main_frame, text="Type Here", padding="5")
            text_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
            
            self.text_area = scrolledtext.ScrolledText(text_frame, height=8, width=80)
            self.text_area.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.text_area.bind('<KeyPress>', self.on_key_press)
            self.text_area.bind('<KeyRelease>', self.on_key_release)
            
            # Current word display
            current_word_frame = ttk.LabelFrame(main_frame, text="Current Word", padding="5")
            current_word_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
            
            self.current_word_label = ttk.Label(current_word_frame, text="", font=("Arial", 14, "bold"))
            self.current_word_label.grid(row=0, column=0)
            
            self.word_status_label = ttk.Label(current_word_frame, text="", font=("Arial", 10))
            self.word_status_label.grid(row=1, column=0)
            
            # Statistics frame
            stats_frame = ttk.LabelFrame(main_frame, text="Typing & Dictionary Statistics", padding="5")
            stats_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
            
            self.stats_text = tk.Text(stats_frame, height=6, width=35, state='disabled')
            self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Word log frame
            word_log_frame = ttk.LabelFrame(main_frame, text="Recent Words", padding="5")
            word_log_frame.grid(row=3, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
            
            self.word_log_text = tk.Text(word_log_frame, height=6, width=35, state='disabled')
            self.word_log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Keystroke log frame
            log_frame = ttk.LabelFrame(main_frame, text="Keystroke Log (Last 10)", padding="5")
            log_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
            
            self.log_text = tk.Text(log_frame, height=4, width=80, state='disabled')
            self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            
            # Control buttons
            button_frame = ttk.Frame(main_frame)
            button_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
            
            ttk.Button(button_frame, text="Clear All", command=self.clear_all).grid(row=0, column=0, padx=(0, 5))
            ttk.Button(button_frame, text="Save Log", command=self.save_log).grid(row=0, column=1, padx=5)
            ttk.Button(button_frame, text="Show Stats", command=self.update_stats).grid(row=0, column=2, padx=5)
            ttk.Button(button_frame, text="Word Analysis", command=self.show_word_analysis).grid(row=0, column=3, padx=(5, 0))
            
            # Configure grid weights
            self.root.columnconfigure(0, weight=1)
            self.root.rowconfigure(0, weight=1)
            main_frame.columnconfigure(0, weight=1)
            main_frame.columnconfigure(1, weight=1)
            main_frame.columnconfigure(2, weight=1)
            main_frame.rowconfigure(2, weight=1)
            main_frame.rowconfigure(3, weight=1)
            main_frame.rowconfigure(4, weight=1)
            text_frame.columnconfigure(0, weight=1)
            text_frame.rowconfigure(0, weight=1)
            stats_frame.columnconfigure(0, weight=1)
            stats_frame.rowconfigure(0, weight=1)
            word_log_frame.columnconfigure(0, weight=1)
            word_log_frame.rowconfigure(0, weight=1)
            log_frame.columnconfigure(0, weight=1)
            log_frame.rowconfigure(0, weight=1)
            
        def on_key_press(self, event):
            if self.start_time is None:
                self.start_time = time.time()
                
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            # Log the keystroke
            keystroke_data = {
                'timestamp': timestamp,
                'key': event.keysym,
                'char': event.char if event.char.isprintable() else f'<{event.keysym}>',
                'event_type': 'press'
            }
            
            self.keystroke_log.append(keystroke_data)
            self.char_count += 1
            
            # Handle word building and completion
            if event.char.isprintable() and event.char not in string.whitespace and event.char not in string.punctuation:
                self.current_word += event.char.lower()
            elif event.char in string.whitespace or event.char in string.punctuation or event.keysym in ['Return', 'Tab']:
                if self.current_word:
                    self.complete_word()
            elif event.keysym == 'BackSpace':
                if self.current_word:
                    self.current_word = self.current_word[:-1]
            
            self.update_current_word_display()
            self.update_log_display()
            
        def on_key_release(self, event):
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            
            keystroke_data = {
                'timestamp': timestamp,
                'key': event.keysym,
                'char': event.char if event.char.isprintable() else f'<{event.keysym}>',
                'event_type': 'release'
            }
            
            self.keystroke_log.append(keystroke_data)
            
        def complete_word(self):
            """Process a completed word"""
            if not self.current_word:
                return
                
            word_data = {
                'word': self.current_word,
                'timestamp': datetime.now().strftime("%H:%M:%S.%f")[:-3],
                'is_valid': self.is_valid_word(self.current_word),
                'length': len(self.current_word)
            }
            
            self.word_log.append(word_data)
            self.typed_words.append(self.current_word)
            
            if word_data['is_valid']:
                self.correct_words += 1
            else:
                self.incorrect_words += 1
                
            self.current_word = ""
            self.update_word_log_display()
            
        def is_valid_word(self, word):
            """Check if a word is in the dictionary"""
            return word.lower() in self.common_words
            
        def update_current_word_display(self):
            """Update the current word being typed"""
            self.current_word_label.config(text=self.current_word if self.current_word else "...")
            
            if self.current_word:
                if self.is_valid_word(self.current_word):
                    self.word_status_label.config(text="✓ Valid word", foreground="green")
                else:
                    # Check for partial matches
                    suggestions = self.get_word_suggestions(self.current_word)
                    if suggestions:
                        self.word_status_label.config(text=f"Suggestions: {', '.join(suggestions[:3])}", foreground="orange")
                    else:
                        self.word_status_label.config(text="? Unknown word", foreground="red")
            else:
                self.word_status_label.config(text="", foreground="black")
                
        def get_word_suggestions(self, partial_word):
            """Get word suggestions based on partial input"""
            suggestions = []
            for word in self.common_words:
                if word.startswith(partial_word.lower()) and word != partial_word.lower():
                    suggestions.append(word)
                    if len(suggestions) >= 5:
                        break
            return suggestions
            
        def update_word_log_display(self):
            """Update the word log display"""
            self.word_log_text.config(state='normal')
            self.word_log_text.delete(1.0, tk.END)
            
            # Show last 10 words
            recent_words = self.word_log[-10:]
            for word_data in recent_words:
                status = "✓" if word_data['is_valid'] else "✗"
                color = "green" if word_data['is_valid'] else "red"
                self.word_log_text.insert(tk.END, f"{status} {word_data['word']}\n")
            
            self.word_log_text.config(state='disabled')
            self.word_log_text.see(tk.END)
            
        def update_log_display(self):
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            
            # Show last 10 keystrokes
            recent_logs = self.keystroke_log[-10:]
            for log in recent_logs:
                if log['event_type'] == 'press':
                    self.log_text.insert(tk.END, f"{log['timestamp']}: {log['char']}\n")
            
            self.log_text.config(state='disabled')
            self.log_text.see(tk.END)
            
        def update_stats(self):
            if not self.keystroke_log or self.start_time is None:
                return
                
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            
            # Calculate statistics
            total_keystrokes = len([log for log in self.keystroke_log if log['event_type'] == 'press'])
            wpm = (total_keystrokes / 5) / (elapsed_time / 60) if elapsed_time > 0 else 0
            
            # Word statistics
            total_words = len(self.typed_words)
            accuracy = (self.correct_words / total_words * 100) if total_words > 0 else 0
            
            stats_text = f"""Session Statistics:

    Time: {elapsed_time:.1f}s
    Keystrokes: {total_keystrokes}
    WPM: {wpm:.1f}

    Word Analysis:
    Total Words: {total_words}
    Correct: {self.correct_words}
    Incorrect: {self.incorrect_words}
    Accuracy: {accuracy:.1f}%

    Avg Keys/Sec: {total_keystrokes/elapsed_time:.1f}
    """
            
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.insert(1.0, stats_text)
            self.stats_text.config(state='disabled')
            
        def show_word_analysis(self):
            """Show detailed word analysis in a popup"""
            if not self.typed_words:
                messagebox.showinfo("Word Analysis", "No words typed yet!")
                return
                
            # Analyze word patterns
            word_freq = {}
            for word in self.typed_words:
                word_freq[word] = word_freq.get(word, 0) + 1
                
            most_common = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Find unique words
            unique_words = len(set(self.typed_words))
            
            # Find longest word
            longest_word = max(self.typed_words, key=len) if self.typed_words else ""
            
            analysis_text = f"""Word Analysis Report:

    Total Words Typed: {len(self.typed_words)}
    Unique Words: {unique_words}
    Longest Word: "{longest_word}" ({len(longest_word)} chars)

    Most Frequently Typed Words:
    """
            
            for word, count in most_common:
                analysis_text += f"  {word}: {count} times\n"
                
            # Show incorrect words
            incorrect_words = [wd['word'] for wd in self.word_log if not wd['is_valid']]
            if incorrect_words:
                analysis_text += f"\nIncorrect Words:\n"
                for word in set(incorrect_words):
                    analysis_text += f"  {word}\n"
            
            # Create popup window
            analysis_window = tk.Toplevel(self.root)
            analysis_window.title("Word Analysis Report")
            analysis_window.geometry("400x500")
            
            text_widget = scrolledtext.ScrolledText(analysis_window, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(1.0, analysis_text)
            text_widget.config(state='disabled')
            
        def clear_all(self):
            self.text_area.delete(1.0, tk.END)
            self.keystroke_log.clear()
            self.word_log.clear()
            self.typed_words.clear()
            self.current_word = ""
            self.start_time = None
            self.char_count = 0
            self.correct_words = 0
            self.incorrect_words = 0
            
            # Clear all displays
            self.stats_text.config(state='normal')
            self.stats_text.delete(1.0, tk.END)
            self.stats_text.config(state='disabled')
            
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.config(state='disabled')
            
            self.word_log_text.config(state='normal')
            self.word_log_text.delete(1.0, tk.END)
            self.word_log_text.config(state='disabled')
            
            self.current_word_label.config(text="")
            self.word_status_label.config(text="")
            
        def save_log(self):
            if not self.keystroke_log and not self.word_log:
                messagebox.showwarning("Save Log", "No data to save!")
                return
                
            filename = f"enhanced_typing_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            data_to_save = {
                'keystroke_log': self.keystroke_log,
                'word_log': self.word_log,
                'session_stats': {
                    'total_words': len(self.typed_words),
                    'correct_words': self.correct_words,
                    'incorrect_words': self.incorrect_words,
                    'unique_words': len(set(self.typed_words)),
                    'session_duration': time.time() - self.start_time if self.start_time else 0
                }
            }
            
            try:
                with open(filename, 'w') as f:
                    json.dump(data_to_save, f, indent=2)
                messagebox.showinfo("Save Log", f"Enhanced log saved to {filename}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Error saving log: {e}")

def main():
        root = tk.Tk()
        app = Keylogger(root)
        
       
        
        root.mainloop()

if __name__ == "__main__":
        main()