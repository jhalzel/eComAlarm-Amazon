import React, { createContext, useState, useEffect, useContext } from 'react'

// Create context
const ThemeContext = createContext()

// Provider component
export function ThemeProvider({ children }) {
  const [isdark, setIsdark] = useState(
    JSON.parse(localStorage.getItem('isdark')) || false
  )

  useEffect(() => {
    localStorage.setItem('isdark', JSON.stringify(isdark))
    document.documentElement.setAttribute('data-theme', isdark ? 'dim' : 'nord')
  }, [isdark])

  return (
    <ThemeContext.Provider value={{ isdark, setIsdark }}>
      {children}
    </ThemeContext.Provider>
  )
}

// Custom hook for consuming the theme context
export function useTheme() {
  return useContext(ThemeContext)
}
