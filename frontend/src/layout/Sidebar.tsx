import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import icons from "./Icons";

interface SectionItem {
  name: string;
  path: string;
  icon: React.ReactNode;
}

interface Section {
  title: string;
  path: string;
  icon: React.ReactNode;
  items: SectionItem[];
  // allowedGroups?: string[];
}

const Sidebar: React.FC = () => {


  const [isCollapsed, setIsCollapsed] = useState<boolean>(() => {
    try {
      return JSON.parse(localStorage.getItem("sidebarCollapsed") || "false");
    } catch {
      return false;
    }
  });

  const [openSections, setOpenSections] = useState<Record<string, boolean>>({});

  useEffect(() => {
    localStorage.setItem("sidebarCollapsed", JSON.stringify(isCollapsed));
  }, [isCollapsed]);

  const toggleSidebar = () => {
    setIsCollapsed((prev) => !prev);
  };

  const toggleSection = (section: string) => {
    if (!isCollapsed) {
      setOpenSections((prev) => ({
        ...prev,
        [section]: !prev[section],
      }));
    }
  };


  const sections: Section[] = [
    {
      title: "Dashboard",
      path: "/dashboard/",
      icon: icons.Inventory,
      items: [{ name: "Dashboard", path: "/dashboard", icon: icons.Inventory }],
    },
  ];

  return (
    <div
      id="sidebar"
      className={`${isCollapsed ? "w-16" : "w-44"} bg-white text-black p-2 transition-all duration-300 h-full flex flex-col`}
    >
      <button
        onClick={toggleSidebar}
        className="self-end p-2 mb-4 text-black rounded cursor-pointer hover:bg-gray-100"
        aria-label="Toggle Sidebar"
        aria-expanded={!isCollapsed}
      >
        {isCollapsed ? ">" : "<"}
      </button>

      <ul className="space-y-2 flex-1">
        {sections.map((section) => (
          <li className="text-sm" key={section.title} title={section.title}>
            <button
              onClick={() => toggleSection(section.title)}
              className="flex items-center w-full p-2 py-2 rounded hover:bg-gray-100"
            >
              {isCollapsed ? (
                <Link to={section.path} className="flex justify-center w-full">
                  {section.icon}
                </Link>
              ) : (
                <>
                  <span>{section.title}</span>
                  <span className="ml-auto text-[8px]">
                    {openSections[section.title] ? "▲" : "▼"}
                  </span>
                </>
              )}
            </button>

            {!isCollapsed && openSections[section.title] && (
              <ul className="mt-2 ml-2 space-y-1">
                {section.items.map((item) => (
                  <li key={item.name}>
                    <Link to={item.path} className="flex items-center p-2 text-black rounded hover:bg-gray-100">
                      {item.icon && <span className="mr-4 text-[6px]">{item.icon}</span>}
                      {item.name}
                    </Link>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
