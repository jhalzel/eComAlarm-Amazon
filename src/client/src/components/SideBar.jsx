import React from 'react'
import { useAuth } from '../context/authContext'
import { doSignOut } from '../firebase/auth'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { toggleDrawer } from './HamburgerButton'

export default function SideBar() {
	const { userLoggedIn } = useAuth()
	const navigate = useNavigate()
	const handleLogout = async () => {
		toggleDrawer() // Call this function first
		try {
			await doSignOut() // Await sign out completion
			navigate('/login') // Navigate after sign out
		} catch (error) {
			// Handle any errors that occur during sign out
			console.error('Sign out failed:', error)
		}
	}

	return (
		<>
			<input id="my-drawer" type="checkbox" className="drawer-toggle" />
			{/* Page content here */}
			<label htmlFor="my-drawer" className="btn btn-link group h-7 w-14 rounded-lg border-2">
				<div className="grid justify-items-center gap-1.5">
					<span className="h-1 w-8 rounded-full bg-neutral-content  transition group-hover:rotate-45 group-hover:translate-y-2.5"></span>

					<span className="h-1 w-8 rounded-full bg-neutral-content  group-hover:scale-x-0 transition"></span>

					<span className="h-1 w-8 rounded-full bg-neutral-content   group-hover:-rotate-45 group-hover:-translate-y-2.5"></span>
				</div>
			</label>
			{/* </div> */}
			<div className="drawer-side z-10">
				<label
					htmlFor="my-drawer"
					aria-label="close sidebar"
					className="drawer-overlay z-100"></label>
				<ul className="menu bg-base-200 text-base-content min-h-full w-80 p-4">
					{userLoggedIn ? (
						<>
							<li>
								<Link onClick={toggleDrawer} to="/home">
									Sales Dashboard
								</Link>
							</li>
							<li>
								<Link onClick={toggleDrawer} to="/scanner">
									Scanner
								</Link>
							</li>
							<li>
								<button onClick={handleLogout}>Log Out</button>
							</li>
						</>
					) : (
						<>
							<li>
								<Link onClick={toggleDrawer} to="/login">
									HomePage
								</Link>
							</li>
							<li>
								<Link onClick={toggleDrawer} to="/login">
									Login / Register
								</Link>
							</li>
						</>
					)}
				</ul>
			</div>
		</>
	)
}
