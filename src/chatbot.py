import os
import requests
from groq import Groq
from dotenv import load_dotenv
from chatbot_modes import CompanyMode, GeneralMode

class Chatbot:
    def __init__(self, company_data, mode="Company Assistant"):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.company_data = company_data
        self.mode = CompanyMode(company_data) if mode == "Company Assistant" else GeneralMode(company_data)
        # Only prepare context once when needed
        self._context = None

    @property
    def context(self):
        if self._context is None:
            self._context = self._prepare_context()
        return self._context

    def _prepare_context(self):
        """Prepare company context for the chatbot"""
        # Get development services names
        dev_services = [service['name'] for service in self.company_data['expertise']['development']]
        
        # Get industry names
        industries = [industry['name'] for industry in self.company_data['expertise']['industries']]
        
        # Get all unique technologies
        technologies = set()
        for service in self.company_data['expertise']['development']:
            technologies.update(service['technologies'])
        
        context = f"""
        You are an expert technical consultant and representative for {self.company_data['company_name']}.
        
        Company Profile:
        Name: {self.company_data['company_name']}
        Description: {self.company_data['description']}
        
        Core Expertise:
        Development Services: {', '.join(dev_services)}
        Industry Focus: {', '.join(industries)}
        Technology Stack: {', '.join(sorted(technologies))}
        
        Frequently Asked Questions:
        """
        
        for faq in self.company_data['faqs']:
            context += f"\nQ: {faq['question']}\nA: {faq['answer']}\n"
        
        # Add contact information
        context += "\nContact Information:\n"
        contact = self.company_data['contact']
        context += f"Email: {contact['email']}\n"
        context += f"Support: {contact['support_email']}\n"
        context += f"Sales: {contact['sales_email']}\n"
        context += f"Phone: {contact['phone']['main']}\n"
        context += f"Website: {contact['website']}\n"
        
        context += """
        
        Instructions:
        1. Provide detailed, technical yet accessible answers
        2. Focus on our software development expertise and capabilities
        3. Highlight relevant technologies and methodologies when appropriate
        4. Maintain a professional and confident tone
        5. If unsure about specific details, provide general industry best practices
        6. Always prioritize accuracy and honesty in responses
        """
        
        return context

    def get_response(self, question, message_history):
        """Generate response using Groq API"""
        try:
            # Get focused context based on question
            context_focus = self._get_focused_context(question.lower())
            
            # Get mode-specific system prompt
            system_prompt = self.mode.get_system_prompt(context_focus)
            
            # Include recent conversation history for context
            conversation = [
                {"role": msg["role"], "content": msg["content"]} 
                for msg in message_history[-3:]  # Keep last 3 messages for context
            ]
            
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    *conversation,
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.7,
                "top_p": 0.9
            }

            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                content = response.json()['choices'][0]['message']['content']
                # Clean up formatting
                content = content.replace('**', '')
                content = content.replace('====', '')
                content = content.replace('----', '')
                return content
            else:
                error_message = response.json().get('error', {}).get('message', 'Unknown error')
                return f"Error: {error_message} (Status code: {response.status_code})"
                
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"

    def _get_focused_context(self, question):
        """Get focused context based on question type"""
        context_parts = []
        
        # Add company name and description always
        context_parts.append(f"Company: {self.company_data['company_name']}")
        
        # Check question type and add relevant context
        if any(word in question for word in ['cost', 'price', 'payment', 'budget']):
            context_parts.append("Pricing: " + next(faq['answer'] for faq in self.company_data['faqs'] if 'cost' in faq['question'].lower()))
        
        elif any(word in question for word in ['security', 'compliance', 'protection']):
            context_parts.append("Security: " + next(faq['answer'] for faq in self.company_data['faqs'] if 'security' in faq['question'].lower()))
        
        elif any(word in question for word in ['technology', 'tech stack', 'programming']):
            context_parts.append("Technologies: " + ', '.join(self.company_data['expertise']['technologies']))
        
        elif any(word in question for word in ['support', 'maintenance']):
            context_parts.append("Support: " + next(faq['answer'] for faq in self.company_data['faqs'] if 'support' in faq['question'].lower()))
        
        # Add relevant metrics if available
        if 'achievements' in self.company_data:
            relevant_metrics = {k: v for k, v in self.company_data['achievements']['metrics'].items() if k.lower() in question}
            if relevant_metrics:
                context_parts.append("Metrics: " + str(relevant_metrics))
        
        return ' | '.join(context_parts) 