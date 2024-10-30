import React, { useState } from 'react';
//import logo from './logo.svg';
import './App.css';
import { searchProduct, placeOrder } from './snsMock';

function App() {
  
  const [productID, setProductID] = useState('');
  const [productName, setProductName] = useState('');
  const [quantity, setQuantity] = useState('');

  const handleSearchProduct = () => {
    console.log("Search product clicked");
    searchProduct(productID, productName);
  };

  const handlePlaceOrder = () => {
    console.log("Place order clicked");
    placeOrder(productID, quantity);
  };
  

  return (
    <div className="App">
      <header className="App-header">
        <p>
          e-commerce
        </p>
      </header>
      <div>
        <h2>Search Product</h2>
        <input
          type="text"
          placeholder="Product ID"
          value={productID}
          onChange={(e) => setProductID(e.target.value)}
        />
        <input
          type="text"
          placeholder="Product Name"
          value={productName}
          onChange={(e) => setProductName(e.target.value)}
        />
        <button onClick={handleSearchProduct}>Search Product</button>
      </div>
      <div>
        <h2>Place Order</h2>
        <input
          type="text"
          placeholder="Product ID"
          value={productID}
          onChange={(e) => setProductID(e.target.value)}
        />
        <input
          type="number"
          placeholder="Quantity"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />
        <button onClick={handlePlaceOrder}>Place Order</button>
      </div>
    </div>
  );
}

export default App;