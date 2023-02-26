import React, { useState } from 'react'
import './SearchBar.css'

const SearchBar = () => {
    const [searchInput, setSearchInput] = useState("");

    const handleChange = (e) => {
        e.preventDefault();
        setSearchInput(e.target.value);
    };

return <div>
    <input 
        id="search_bar"
        type="text"
        size="100"
        placeholder="Enter Unknown Object Here..."
        onChange={handleChange}
        value={searchInput} />
</div>
};

export default SearchBar;

