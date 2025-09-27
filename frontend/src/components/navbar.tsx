import { Link } from "@tanstack/react-router";

const navigation = [
  { name: "Matches", href: "/matches/" },
  { name: "Teams", href: "/teams/" },
  { name: "Players", href: "/players/" },
];

export default function Navbar() {
  return (
    <div className="flex flex-row items-center justify-between py-1">
      <div className="w-1/3">
        <Link to="/">
          <img
            src="/src/assets/images/logo.png"
            className="size-12"
            alt="logo"
          />
        </Link>
      </div>
      <div className="flex w-1/3 flex-row justify-center space-x-4">
        {navigation.map((item) => (
          <Link
            to={item.href}
            className="text-neutral-400 hover:text-white"
            activeProps={{
              className:
                "text-purple-50 underline underline-offset-8 decoration-blue-600 decoration-4",
            }}
          >
            {item.name}
          </Link>
        ))}
      </div>
      <div className="w-1/3"></div>
    </div>
  );
}
