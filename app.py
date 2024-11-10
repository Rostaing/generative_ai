from llm_axe import OnlineAgent, OllamaChat, PdfReader
from llm_axe.models import OllamaChat
from llm_axe.core import read_pdf, safe_read_json
from llm_axe.agents import DataExtractor, Agent
from llm_axe.core import AgentType

# 1er cas

llm = OllamaChat(model="llama3.2:latest")

# data = read_pdf("reçu.pdf")
# de = DataExtractor(llm, reply_as_json=True)
# resp = de.ask(data, ["Date de la transaction", "Référence de la transaction", "Identifiant de la commande", "Identifiant du commersgant"
#                      "Cas de paiement", "Montant de la transaction", "Numéro d’autorisation"])

# print(resp)

# 2ème cas

# read_pdf = PdfReader(llm)
# resp = read_pdf.ask("Quel est le montant de la transaction de cette facture ?", ["reçu.pdf"])
# print(resp)

# 3ème cas

# online_agent = OnlineAgent(llm)
# prompt = "Donne-moi les dernières nouvelles sur la Data Science."
# resp = online_agent.search(prompt)
# print(resp)

# 4ème cas

prompt = "Calcule et imprime l'âge du père et l'âge de son fils sachant que le père a n années de plus que son fils et que dans m années il aura k fois l'âge du fils."

# Planner Agent

# planner = Agent(llm, agent_type=AgentType.PLANNER)
# resp = planner.ask(prompt)
# print(resp)

# 5ème cas
generic_responder = Agent(llm, agent_type=AgentType.GENERIC_RESPONDER)
resp = generic_responder.ask(prompt)
print(resp)