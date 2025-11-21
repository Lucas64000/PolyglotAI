
import json
import os
import threading
from typing import List, Dict
from uuid import UUID
from pathlib import Path

from src.models.user_model import User

from .repository_interface import BaseMemoryRepository
from src.models.conversation_model import Conversation, Message
from src.utils.logger import get_logger
from src.core.enums import ConversationStatus

logger = get_logger(__name__)

class JsonFileMemoryRepository(BaseMemoryRepository):
    "Stocke chaque user et conversation dans un fichier JSON séparé."
    def __init__(self, base_dir: str = "data"):
        self.base_dir = Path(base_dir)
        self.conversations_dir = self.base_dir / "conversations"
        self.users_dir = self.base_dir / "users"
        
        self._lock = threading.RLock()
        
        self._ensure_directory_exists(self.conversations_dir)
        self._ensure_directory_exists(self.users_dir)

        # Index en mémoire
        self._conversations_index: Dict[str, Conversation] = {} 
        self.index_file_path = self.conversations_dir / "conversations_index.json"

        self._load_index()

    def _ensure_directory_exists(self, path: Path):
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)

    # =============================================
    # CRUD CONVERSATIONS
    # =============================================

    def _load_index(self):    
        """Charge l'index des conversations (sans les messages)"""
        if not self.index_file_path.exists():
            return
        
        with self._lock:
            try:
                with open(self.index_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    for conv_data in data:
                        conv = Conversation.model_validate(conv_data)
                        self._conversations_index[str(conv.id)] = conv

                logger.info(f"Chargé {len(self._conversations_index)} métadonnées de conversations")

            except Exception as e:
                logger.error(f"Erreur lors du chargement de l'index des conversations: {e}")
                self._conversations_index = {}

    def _save_index(self):
        """Sauvegarde les métadonnées des conversations sur le disque"""
        with self._lock:
            try:
                data_to_save = [
                    conv.model_dump(mode="json") for conv in self._conversations_index.values()
                    if conv.status != ConversationStatus.DELETED
                ]
            
                with open(self.index_file_path, 'w', encoding='utf-8') as f:
                    json.dump(data_to_save, f, ensure_ascii=False, indent=2)
            
            except Exception as e:
                logger.error(f"Erreur lors de la sauvegarde de l'index des conversations: {e}")

    def _get_conversation_file_path(self, conversation_id: UUID) -> Path:
        """Retourne le chemin du fichier pour une conversation donnée."""
        return self.conversations_dir / f"{str(conversation_id)}.json"

    def _load_conversation(self, conversation_id: UUID) -> List[Message]:
        """Charge une conversation depuis son fichier."""
        file_path = self._get_conversation_file_path(conversation_id)
        
        if not file_path.exists():
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Message.model_validate(msg) for msg in data]
        except Exception as e:
            logger.error(f"Erreur lecture fichier {file_path}: {e}")
            return []

    def _save_conversation(self, conversation_id: UUID, messages: List[Message]):
        """Sauvegarde une conversation dans son fichier."""
        file_path = self._get_conversation_file_path(conversation_id)
        
        try:
            data_to_save = [msg.model_dump(mode='json') for msg in messages]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"Erreur écriture fichier {file_path}: {e}")

    def _delete_conversation_file(self, conversation_id: UUID) -> None:
        file_path = self._get_conversation_file_path(conversation_id)

        if file_path.exists():
            os.remove(file_path)
            logger.info(f"Historique des messages de la conversation {conversation_id} supprimé")

    def create_conversation(self, user_id: UUID) -> Conversation:
        
        if not self._user_exists(user_id):
            raise ValueError(f"Impossible de créer une conversation: l'utilisateur {user_id} n'existe pas")
        
        conv = Conversation(user_id=user_id)

        with self._lock:
            self._conversations_index[str(conv.id)] = conv
            self._save_index()
            self._load_index()

        logger.info(f"Conversation {conv.id} créée pour l'utilisateur {user_id}")
        return conv

    def get_all_conversations(self, user_id: UUID) -> List[Conversation]:
        with self._lock:
            conversations = list(self._conversations_index.values())
            
            filtered_conversations = [
                conv for conv in conversations 
                if conv.user_id == user_id and conv.status != ConversationStatus.DELETED 
            ]

            # Tri des conversations par date pour que la plus récente soit en premier
            return sorted(filtered_conversations, key=lambda c: c.created_at, reverse=True)

    def get_conversation_by_id(self, conversation_id: UUID) -> Conversation:
        cid_str = str(conversation_id)

        with self._lock:
            if cid_str not in self._conversations_index:
                logger.warning(f"Conversation {cid_str} introuvable")
                raise ValueError(f"La conversation {conversation_id} n'existe pas.")
            
            return self._conversations_index[cid_str]
        
    def update_conversation_metadata(self, updated_conversation: Conversation) -> None:
        cid_str = str(updated_conversation.id)

        if cid_str not in self._conversations_index:
            logger.warning(f"Conversation {cid_str} introuvable")
            return
        
        with self._lock:
            self._conversations_index[cid_str] = updated_conversation
            self._save_index()
            logger.debug(f"Conversation {cid_str} mise à jour")

    def delete_conversation(self, conversation_id: UUID) -> None:
        cid_str = str(conversation_id)
        
        with self._lock:
            if cid_str in self._conversations_index:
                del self._conversations_index[cid_str]

                self._delete_conversation_file(conversation_id)
                self._save_index()
        logger.debug(f"Conversation {conversation_id} supprimée")

    # =============================================
    # CRUD MESSAGES
    # =============================================

    def save_message(self, message: Message) -> None:
        """
        Ajoute un message à l'historique de conversation
        """
        cid = message.conversation_id
        
        with self._lock:
            messages = self._load_conversation(cid) 
            messages.append(message)
            self._save_conversation(cid, messages)
            
            logger.debug(f"Message sauvegardé dans {cid}.json")

    def get_messages(self, conversation_id: UUID) -> List[Message]:
        """Lit le fichier spécifique et retourne les messages"""
        with self._lock:
            messages = self._load_conversation(conversation_id)
            return sorted(messages, key=lambda m: m.created_at)

    def update_message(self, new_message: Message) -> None:
        """Update et supprime les messages suivants"""
        cid = new_message.conversation_id
        
        with self._lock:
            messages = self._load_conversation(cid)
            
            target_index = next((i for i, m in enumerate(messages) if m.id == new_message.id), -1)
            
            if target_index == -1:
                logger.warning(f"Update impossible: Message {new_message.id} introuvable.")
                return

            updated_messages = messages[:target_index] + [new_message]
            
            self._save_conversation(cid, updated_messages)
            logger.info(f"Conversation {cid} mise à jour")

    # =============================================
    # CRUD USERS
    # =============================================


    def _get_user_file_path(self, user_id: UUID) -> Path:
        """Récupère le json de l'utilisateur."""
        return self.users_dir / f"{str(user_id)}.json"

    def _user_exists(self, user_id: UUID) -> bool:
        """Vérifie si un utilisateur existe."""
        file_path = self._get_user_file_path(user_id)
        return file_path.exists()
    
    def create_user(self, user: User) -> None:
        """Créé un utilisateur."""
        file_path = self._get_user_file_path(user.id)
        if file_path.exists():
            raise ValueError(f"Impossible de créer l'utilsateur {user.name} avec l'ID {user.id} : il existe déjà.")
        
        with self._lock:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(user.model_dump_json(indent=2))
                logger.debug(f"Utilisateur {user.id} sauvegardé.")
            except Exception as e:
                logger.error(f"Erreur sauvegarde user {user.id}: {e}")


    def get_user(self, user_id: UUID) -> User:
        """Récupère un utilisateur par son ID."""
        file_path = self._get_user_file_path(user_id)
        
        if not file_path.exists():
            logger.warning(f"Utilisateur {user_id} introuvable.")
            raise ValueError(f"L'utilisateur {user_id} n'existe pas")
        
        with self._lock:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return User.model_validate(data)
            except Exception as e:
                logger.error(f"Erreur chargement user {user_id}: {e}")
                raise ValueError(f"Erreur lors du chargement de l'utilisateur {user_id}") from e