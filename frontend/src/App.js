import React, { useState } from 'react';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Card, ListGroup, Spinner, Alert, Navbar, Nav, Modal } from 'react-bootstrap';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [message, setMessage] = useState('');
  const [products, setProducts] = useState([]);
  const [skinTone, setSkinTone] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(''); // Error handling state
  const [showGenderModal, setShowGenderModal] = useState(false); // Modal state
  const [gender, setGender] = useState(null); // Store selected gender

  // Handle file selection and preview
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setImagePreview(URL.createObjectURL(file));
  };

  // Handle gender selection
  const handleGenderSelect = (selectedGender) => {
    setGender(selectedGender);
    setShowGenderModal(false); // Close the modal after selection
    processImage(selectedFile, selectedGender); // Call the function to process the image after gender is selected
  };

  // Handle file upload and receive product suggestions
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setMessage("Please select a file first.");
      return;
    }

    setShowGenderModal(true); // Show the gender selection modal after upload
  };

  // Process image after gender selection
  const processImage = async (file, selectedGender) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('gender', selectedGender); // Send gender as part of the request

    setLoading(true); // Show loading spinner
    setError(''); // Reset error state

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.message && response.data.skinTone) {
        setMessage(response.data.message);
        setSkinTone(response.data.skinTone); // Set skin tone color
      } else {
        throw new Error("Unexpected response format from the server");
      }
    } catch (error) {
      console.error("There was an error uploading the file!", error);
      setError("Error uploading file. Please try again.");
    } finally {
      setLoading(false); // Hide loading spinner
    }
  };

  return (
    <div style={{ backgroundColor: '#fff', minHeight: '100vh', padding: '0rem 0' }}>
      {/* Navbar with Left Logo and Right Links */}
      <Navbar expand="lg" className="gradient-navbar mb-4 navbar-custom">
        <Navbar.Brand href="#home" className="navbar-brand-custom"></Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
          <Nav>
            <Nav.Link href="#home"></Nav.Link>
            <Nav.Link href="#about"></Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Navbar>

      <Container className="container mt-5">
        <Row className="justify-content-center">
          {/* Main Form and Image Preview */}
          <Col md={6}>
            <Card className="card shadow-sm p-4 mb-4">
              <h2 className="text-center mb-4">Upload Your Photo</h2>
              <Form onSubmit={handleUpload}>
                <Form.Group controlId="formFile" className="mb-3">
                  <Form.Label>Select a photo to upload</Form.Label>
                  <Form.Control type="file" onChange={handleFileChange} />
                </Form.Group>
                <Button variant="primary" type="submit" className="w-100 mb-4">
                  {loading ? (
                    <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                  ) : (
                    'Upload'
                  )}
                </Button>
              </Form>

              {imagePreview && (
                <Card className="mb-3">
                  <Card.Img variant="top" src={imagePreview} alt="Uploaded Preview" className="card-img" />
                </Card>
              )}

              {message && (
                <Alert variant="info" className="mt-3">
                  {message}
                </Alert>
              )}

              {/* Display any error message */}
              {error && (
                <Alert variant="danger" className="mt-3">
                  {error}
                </Alert>
              )}
            </Card>
          </Col>

          {/* Side Column for Skin Tone */}
          <Col md={3}>
            <Card className="card shadow-sm p-4 mb-4">
              <h4 className="mb-3 text-center">Detected Skin Tone</h4>
              {loading ? (
                <div className="d-flex justify-content-center">
                  <Spinner animation="border" />
                </div>
              ) : (
                skinTone && (
                  <div
                    className="skin-tone-display p-3"
                    style={{
                      backgroundColor: skinTone,
                      borderRadius: "10px",
                      height: "100px",
                    }}
                  >
                    {/* Display the skin tone color */}
                  </div>
                )
              )}
            </Card>
          </Col>

          {/* Side Column for Product Recommendations */}
          <Col md={3}>
            <Card className="card shadow-sm p-4 mb-4">
              <h4 className="mb-3 text-center">Outfit Suggestions</h4>
              {loading ? (
                <div className="d-flex justify-content-center">
                  <Spinner animation="border" />
                </div>
              ) : (
                products.length > 0 && (
                  <ListGroup variant="flush">
                    {products.map((product, index) => (
                      <ListGroup.Item key={index}>{product}</ListGroup.Item>
                    ))}
                  </ListGroup>
                )
              )}
            </Card>
          </Col>
        </Row>
      </Container>

      {/* Gender Selection Modal */}
      <Modal show={showGenderModal} onHide={() => setShowGenderModal(false)} centered>
        <Modal.Header closeButton>
          <Modal.Title>Select Your Gender</Modal.Title>
        </Modal.Header>
        <Modal.Body className="text-center">
          <Button variant="primary" className="m-2" onClick={() => handleGenderSelect('male')}>
            Male
          </Button>
          <Button variant="secondary" className="m-2" onClick={() => handleGenderSelect('female')}>
            Female
          </Button>
        </Modal.Body>
      </Modal>
    </div>
  );
}

export default App;
