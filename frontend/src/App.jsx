import { useEffect, useState } from 'react'
import ContactList from './ContactList'
import './App.css'
import ContactForm from './ContactForm'

function App() {
  const [contacts, setContacts] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentContact, setCurrentContact] = useState({})

  useEffect(() => {
    fetchContacts()
  }, [])

  const fetchContacts = async () => {
    const response = await fetch("http://127.0.0.1:5000/contacts");
    const data = await response.json();
    setContacts(data.contacts);
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentContact({})
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModel = (contact) => {
    if (isModalOpen) return
    setCurrentContact(contact)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchContacts()
  }

  return (<><ContactList contacts={contacts} updateContact={openEditModel} updateCallback={onUpdate}/>
  <button onClick={openCreateModal}>Create New Contact</button>
  { isModalOpen && <div className="modal">
  <div className="modal-content">
    <span className="close" onClick={closeModal}>&times;</span>
    <ContactForm existingContact={currentContact} updateCallback={onUpdate}/>
  </div>
  </div>

  }
    </>);
}

export default App
