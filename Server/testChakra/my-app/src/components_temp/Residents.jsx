import React, { useState, useEffect } from "react";
import axios from "axios";
import { Box, Heading, VStack, HStack, Text, Grid, Image, Button, Spacer, useDisclosure,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalFooter,
    ModalBody,
    ModalCloseButton,
    Checkbox,
    Input,
    Divider
 } from "@chakra-ui/react";

function Residents() {
    const [residents, setResidents] = useState([]);
    const { isOpen, onOpen, onClose } = useDisclosure()
    const [ selected, setSelected] = useState([]);
    const [visitors, setVisitors] = useState([]);
    const [newName, setNewName] = useState("");

    useEffect(() => {
        axios.get("http://localhost:5002/api/residents", { withCredentials: true })
        .then((response) => {setResidents(response.data); console.log(typeof(residents))})
        .catch((error) => { console.error("Error fetching residents:", error);});
        
        axios.get("http://localhost:5002/api/visitors", { withCredentials: true})
        .then((response) => setVisitors(response.data));
    }, []);

    const handleResidentDelete = (name) => {
    // TODO
    console.log("deleting: " + name);
  };

  const handleResidentAdd = (e) =>{
    // TODO
    console.log("adding: " + selected);
    console.log("with name: " + newName);

    onClose(e); 
    setNewName(""); 
    setSelected("");
  }
  const handleSelect = (added, id) =>{
    if (added){
        console.log("selected" + id);
        //add id to selected photos
        setSelected([...selected, id]);
    }else{
        console.log("deselected" + id);
        //remove id from selected photos
        setSelected(selected.filter(a => a!== id));
    }
  }
  const handleNameChange = (event) => {
    setNewName(event.target.value);
  }

  return (
 <Box p={5}>
    <Text fontSize="2xl" fontWeight="bold" mb={4}>Residents</Text>      

      <VStack spacing={3} align="start" width="100%">
        <Button onClick={onOpen}>Add Resident / Add Photos to Existing Residents</Button>
        <Modal isOpen={isOpen} onClose={onClose} size="xl">
        <ModalOverlay />
        <ModalContent>
            {/* Currently, this can also append photos to existing residents */}
            <ModalHeader>Adding/Updating a Resident</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
            Type a name for the new/existing resident
                <Input
                    placeholder="Type a name..."
                    value={newName}
                    onChange={handleNameChange}
                />
                Select images to create a new resident with
                <Grid templateColumns="repeat(auto-fill, minmax(100px, 1fr))" gap={4}>
                        {visitors.map((photo, index) => (
                            <Checkbox key={index} onChange={e => {handleSelect(e.target.checked, photo.id)}}>
                                {photo.timestamp}
                                <Image src={`data:image/png;base64,${photo.data}`} alt={photo.timestamp} borderRadius="md" />
                            </Checkbox>
                        ))}
                </Grid>
            </ModalBody>

            <ModalFooter>
            <Button colorScheme='blue' mr={3} onClick={handleResidentAdd}>
                Save(To do)
            </Button>
            <Button colorScheme='red' onClick={() => {setSelected([])}}>Cancel</Button>
            </ModalFooter>
        </ModalContent>
        </Modal>

        {residents.map((resident, index) => (
        <Box key={index} bg="white" p={4} borderRadius="md" width="100%">
            <HStack>
                <Heading size="md" mb={4} color="brand.darkBlue">
                    {resident.name}
                </Heading>
                <Spacer />
                <Button colorScheme="red" onClick={() => {handleResidentDelete(resident.name)}}>Delete resident(To do)</Button>
            </HStack>
            <Divider p={3}/>
            <Grid templateColumns="repeat(auto-fill, minmax(100px, 1fr))" gap={4}>
                {resident.images.map((photo, index) => (
                <Box key={index} textAlign="center" bg="brand.beige" borderRadius="md">
                    <Image src={`data:image/png;base64,${photo.data}`} borderRadius="md" />
                </Box>
                ))}
            </Grid>
            </Box>
        ))}

    </VStack>
    </Box>

  );
}

export default Residents;
