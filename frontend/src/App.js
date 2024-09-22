import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  Row,
  Col,
  Form,
  Button,
  Card,
  ListGroup,
  Spinner,
  Alert,
  Modal,
  Navbar,
  Nav, // Added Nav for the Navbar links
} from "react-bootstrap";
import "./App.css";
import logo from "./images/logo.png"; // Import your logo

function App() {
  // State hooks for managing app data
  const [selectedFile, setSelectedFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [message, setMessage] = useState("");
  const [products, setProducts] = useState([]);
  const [skinTone, setSkinTone] = useState(null);
  const [colorRecommendation, setColorRecommendation] = useState([]); // Updated to handle multiple colors
  const [seasonMatched, setSeasonMatched] = useState(""); // New state for season matched
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showGenderModal, setShowGenderModal] = useState(false);
  const [showColorModal, setShowColorModal] = useState(false); // Modal for color preview
  const [selectedColor, setSelectedColor] = useState(""); // For selected color in the pop-up
  const [showColorTheoryModal, setShowColorTheoryModal] = useState(false); // Modal for Color Theory
  const [meanings, setMeanings] = useState([]); // New state to store color meanings


  const PEXELS_API_KEY =
    "pGWgqahVrcprpx2XmPB4K8lrs9onLLjwBYRdusShqrglMavLjNpYtEIH";

  // Handle file selection and image preview
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setImagePreview(URL.createObjectURL(file)); // Show image preview
  };

  // Handle gender selection from the modal
  const handleGenderSelect = (selectedGender) => {
    setShowGenderModal(false); // Close the gender selection modal
    processImage(selectedFile, selectedGender); // Process the image with the selected gender
  };

  // Handle file upload, showing gender modal afterward
  const handleUpload = (e) => {
    e.preventDefault();
    if (!selectedFile) {
      setMessage("Please select a file first.");
      return;
    }
    setShowGenderModal(true); // Show gender selection modal
  };

  // Process the uploaded image after gender selection
  const processImage = async (file, selectedGender) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("gender", selectedGender); // Send gender as part of the request
  
    setLoading(true); // Show loading spinner
    setError(""); // Reset error state
  
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );
  
      if (response.data.message && response.data.skinTone) {
        setMessage(response.data.message);
        setSkinTone(response.data.skinTone); // Set skin tone color
  
        const colorData = response.data.color_recommendation; // Get color recommendation array
        setColorRecommendation(colorData); // Set the colors for the frontend
  
        const meaningData = response.data.meanings; // Get the color meanings from the response
        setMeanings(meaningData); // Set the meanings for the frontend
  
        // Add season matched to the state
        setSeasonMatched(response.data.season || "Season not available"); // Set season from the API or provide a fallback
  
        fetchOutfitSuggestions(colorData[0], selectedGender); // Fetch outfits based on the first color and gender
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
  

  // Fetch outfit suggestions using Pexels API
  const fetchOutfitSuggestions = async (colorRecommendation, selectedGender) => {
    try {
      const response = await axios.get("https://api.pexels.com/v1/search", {
        headers: {
          Authorization: PEXELS_API_KEY,
        },
        params: {
          query: `${selectedGender} outfit ${colorRecommendation}`, // Search for outfits based on color and gender
          per_page: 6, // Limit results to 6 images
        },
      });

      const images = response.data.photos.map((photo) => ({
        url: photo.src.medium,
        alt: photo.alt,
      }));

      setProducts(images); // Set the images as product suggestions
    } catch (error) {
      console.error("Error fetching outfit suggestions", error);
      setError("Error fetching outfit suggestions. Please try again.");
    }
  };

  // Handle color click for larger view in a modal
  const handleColorClick = (color) => {
    setSelectedColor(color);
    setShowColorModal(true); // Show the color preview modal
  };

  // Dummy color meanings for the colors
  const colorMeanings = {
    "#FF5733": "Orange represents creativity and enthusiasm.",
    "#33FF57": "Green symbolizes growth, harmony, and freshness.",
    "#3357FF": "Blue conveys tranquility and stability.",
  };

  return (
    <div style={{ backgroundColor: "#edf2f9", minHeight: "100vh", padding: "0rem 0rem" }}>
      {/* Navbar with Logo and Right Links */}
      <Navbar expand="lg" className="gradient-navbar mb-3 navbar-custom">
        <Navbar.Brand href="#home" className="navbar-brand-custom">
          <img
            src={logo}
            alt="CereStyle Logo"
            style={{ width: "150px", height: "auto", padding: "" }} // Set the logo size and padding
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
          <Nav>
            {/* Navbar link to trigger the Color Theory modal */}
            <Nav.Link onClick={() => setShowColorTheoryModal(true)}>About Color Theory</Nav.Link>
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
                <Button
                  style={{ backgroundColor: "#222", color: "#fff" }}
                  type="submit"
                  className="w-100 mb-4"
                >
                  {loading ? (
                    <Spinner
                      as="span"
                      animation="border"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                    />
                  ) : (
                    "Upload"
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

            {/* Color Theory Card placed directly below the Skin Tone Card */}
            <Card className="card shadow-sm p-4 mb-4 mt-3">
              <h4 className="mb-3 text-center">Color Theory</h4>

              {/* Season Matched Section */}
              <h5 className="mt-4">Season Matched:</h5>
              <p>{seasonMatched}</p>

              <h5 className="mt-4">Color Bar</h5>
              <div className="d-flex justify-content-between mt-3">
                {colorRecommendation.length > 0 ? (
                  colorRecommendation.map((color, index) => (
                    <div
                      key={index}
                      className="color-bar"
                      style={{
                        backgroundColor: color,
                        width: "60px",
                        height: "30px",
                        cursor: "pointer",
                      }}
                      onClick={() => handleColorClick(color)}
                    ></div>
                  ))
                ) : (
                  <p>No colors available</p>
                )}
              </div>
            </Card>

            {/* Colors Meaning Card */}
            <Card className="card shadow-sm p-4 mb-4 mt-3">
              <h4 className="mb-3 text-center">Colors Meaning</h4>
              <ListGroup variant="flush">
                {colorRecommendation.length > 0 && meanings.length > 0 ? (
                  colorRecommendation.map((color, index) => (
                    <ListGroup.Item
                      key={index}
                      style={{ backgroundColor: color, color: "#fff" }}
                    >
                      {meanings[index] || "Color meaning not available."}
                    </ListGroup.Item>
                  ))
                ) : (
                  <p>No colors available</p>
                )}
              </ListGroup>
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
                      <ListGroup.Item key={index}>
                        <img src={product.url} alt={product.alt} className="img-fluid" />
                      </ListGroup.Item>
                    ))}
                  </ListGroup>
                )
              )}
            </Card>
          </Col>
        </Row>
      </Container>

      {/* Gender Selection Modal */}
      <Modal
        show={showGenderModal}
        onHide={() => setShowGenderModal(false)}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Select Your Gender</Modal.Title>
        </Modal.Header>
        <Modal.Body className="text-center">
          <Button variant="primary" className="m-2" onClick={() => handleGenderSelect("male")}>
            Male
          </Button>
          <Button variant="secondary" className="m-2" onClick={() => handleGenderSelect("female")}>
            Female
          </Button>
        </Modal.Body>
      </Modal>

      {/* Color View Modal */}
      <Modal
        show={showColorModal}
        onHide={() => setShowColorModal(false)}
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>Color Preview</Modal.Title>
        </Modal.Header>
        <Modal.Body className="text-center">
          <div
            style={{
              backgroundColor: selectedColor,
              width: "100%",
              height: "200px",
              borderRadius: "10px",
            }}
          ></div>
        </Modal.Body>
      </Modal>

       {/* Color Theory Modal */}
       <Modal
        show={showColorTheoryModal}
        onHide={() => setShowColorTheoryModal(false)}
        centered
        size="lg"
      >
        <Modal.Header closeButton>
          <Modal.Title>About Color Theory</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h4>What is Color Theory?</h4>
          <p>
            Color theory is a body of practical guidance to color mixing and
            the visual effects of a specific color combination. Color theory
            principles first appeared in the writings of Leone Battista Alberti
            (c. 1435) and the notebooks of Leonardo da Vinci (c. 1490). A more
            formalized representation of color theory concepts can be found in
            Isaac Newton's color wheel (1704), which maps the relationships
            between colors in a circle.
          </p>
          <p>
            Understanding color theory helps you pair colors more effectively,
            ensuring that your outfits or designs stand out while maintaining
            harmony and visual appeal.
          </p>
          <h5>Primary Colors:</h5>
          <p>Red, Blue, Yellow – these are the base colors that can be mixed to form any other color.</p>
          <h5>Secondary Colors:</h5>
          <p>Orange, Green, Purple – formed by mixing two primary colors.</p>
          <h5>Complementary Colors:</h5>
          <p>
            Colors that sit opposite each other on the color wheel. They create
            high contrast and vibrant looks.
          </p>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowColorTheoryModal(false)}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default App;