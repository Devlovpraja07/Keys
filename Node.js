const express = require("express");
const cors = require("cors");
const { createClient } = require("@supabase/supabase-js");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const supabaseUrl = "https://bzzkdkhwvmzuipfqfvxi.supabase.co";
const supabaseKey =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ6emtka2h3dm16dWlwZnFmdnhpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIyNzQ3MjEsImV4cCI6MjA1Nzg1MDcyMX0.5evL3NbenYZV-BDLR8IpVr_vSFyDowkHV8vZinIMnM0";

const supabase = createClient(supabaseUrl, supabaseKey);

// Get products from Supabase
app.get("/products", async (req, res) => {
  const { data, error } = await supabase.from("products").select("*");
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});

// Add a product
app.post("/products", async (req, res) => {
  const { name, price, image } = req.body;
  const { data, error } = await supabase.from("products").insert([{ name, price, image }]);
  if (error) return res.status(500).json({ error: error.message });
  res.json(data);
});

// Delete a product
app.delete("/products/:id", async (req, res) => {
  const { id } = req.params;
  const { error } = await supabase.from("products").delete().match({ id });
  if (error) return res.status(500).json({ error: error.message });
  res.json({ success: true });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
