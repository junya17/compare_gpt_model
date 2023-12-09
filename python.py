from openai import OpenAI
import gradio as gr #Gradioのインポート
import time 

client = OpenAI() #API keyの取得

class OpenAIChats: #OpenAIChatsクラスの作成
    def generate_text3(self, prompt, temperature): #メソッドの定義
        start_time = time.time()  # レスポンス時間の計測開始
        #OpenAI APIを使うためのコード 
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", #モデル:3.5turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."}, # 役割
                {"role": "user", "content": prompt}, # プロンプト
            ],
            max_tokens=100, # トークンの設定（テキストの長さ）
            temperature=temperature, # 温度の設定：温度が高いと予測不能になる。
        )
        end_time = time.time()  # レスポンス時間の計測終了
        response_time = float(end_time - start_time)  # 浮動小数点数としてレスポンス時間を取得
        return response.choices[0].message.content, response_time # GPTからのレスポンスと時間を返す
    
    def generate_text4(self, prompt ,temperature):
        start_time = time.time()  
        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100, # GPT-4はより詳細な解説をするので長めに設定。
            temperature=temperature,
        )
        end_time = time.time()
        response_time = float(end_time - start_time)
        return response.choices[0].message.content, response_time
    
        # GPT-3とGPT-4の両方の結果を返す関数
    def generate_both_texts(self, prompt, temperature):
        gpt3_response, gpt3_response_time = openai.generate_text3(prompt, temperature)
        gpt4_response, gpt4_response_time = openai.generate_text4(prompt, temperature)
        # 文字列型のレスポンス時間を浮動小数点数に変換
        # フォーマットされたレスポンス時間を返す
        return (gpt3_response, "{:.2f} sec".format(gpt3_response_time),
                gpt4_response, "{:.2f} sec".format(gpt4_response_time)
        )

# OpenAIChatsのインスタンスを作成
openai = OpenAIChats()

# Gradioインターフェースの作成
with gr.Blocks() as gpt_interface: # Blockを使用
    prompt = gr.Textbox(label="Prompt",
                         value="OpenAI is") # プロンプトの入力
    temperature = gr.Slider(minimum=0, 
                            maximum=1, 
                            step=0.1, 
                            value=0.7, 
                            label="Temperature") # 温度をスライドを使って調整
    gpt3 = gr.Textbox(label="GPT-3.5 Turbo") # gpt3のレスポンスを表示
    gpt4 = gr.Textbox(label="GPT-4 Turbo") # gpt4
    gpt3_time = gr.Textbox(label="GPT-3.5 Response Time") #GPT3応答タイムを表示
    gpt4_time = gr.Textbox(label="GPT-4 Response Time") #GPT4
    greet_btn = gr.Button("Chat")
    greet_btn.click(fn=openai.generate_both_texts, 
                    inputs=[prompt, temperature], 
                    outputs=[gpt3, gpt3_time, gpt4, gpt4_time]) # Clickを押すと実行
    
# インターフェースの起動
if __name__ == "__main__":
    gpt_interface.launch(show_api=False)
